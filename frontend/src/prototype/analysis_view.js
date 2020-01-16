import React from "react";
import PropTypes from 'prop-types';

export class SingleValueAnalysis extends React.Component {
    render() {
        let display_value;
        if (this.props.value !== undefined && this.props.round_digits !== undefined) {
            display_value = this.props.value.toFixed(2);
        } else {
            display_value = this.props.value;
        }

        return(
            <div className={"row"}>
                <strong className={"analysis-label col-3"}>
                    {this.props.header}
                </strong>
                <p className={"col-9 mb-1 text-left d-block d-md-inline"}>
                    {display_value} {this.props.unit}
                </p>
            </div>
        );
    }
}
SingleValueAnalysis.propTypes = {
    header: PropTypes.string,
    value: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.string,
    ]),
    unit: PropTypes.string,
    round_digits: PropTypes.number,
};

export class TabularAnalysis extends React.Component{
    render() {
        // Create an array of indices based on the length of the header array
        let range = n => Array.from(Array(n).keys());
        let indices = range(this.props.headers.length);

        const display_object = (_obj) => {
            return (
                <ul>
                    <span>Display me!</span>
                </ul>
            );
        };

        return(
            <div>
                <h3 className={"analysis-subheader mt-4"}> {this.props.title} </h3>
                <table className={"table analysis-table"}>
                    <tbody>
                        <tr>
                            {/* Auto generate the headers */}
                            {this.props.headers.map( (header, k) => (
                                <th className={"p-2"} key={k}>{header}</th>)
                            )}
                        </tr>
                        {this.props.data.map( (entry, k) => (
                            <tr key={k}>
                                {indices.map( (index, k) => (
                                    <td className={"p-2"} key={k}>
                                        {typeof entry[index] === 'object'
                                            ? display_object(entry[index])
                                            : entry[index]
                                        }
                                    </td>)
                                )}
                            </tr>)
                        )}
                    </tbody>
                </table>
            </div>
        );
    }
}
TabularAnalysis.propTypes = {
    headers: PropTypes.array,
    data: PropTypes.array,
    title: PropTypes.string,

};

export class CommonResponses extends React.Component {
    render() {
        return (
            <TabularAnalysis
                title={"Most Common Responses"}
                data={this.props.responses}
                headers={["Question","Context","Answers"]}
            />
        );
    }
}

CommonResponses.propTypes = {
    responses: PropTypes.array,
};

export class FrequencyFeelingTable extends React.Component {
    render() {
        return (
            <div>
                <TabularAnalysis
                    title={ "Frequency Feelings"}
                    headers={["Word","Frequency"]}
                    data={this.props.feelings}
                />
            </div>
        );
    }
}
FrequencyFeelingTable.propTypes = {
    feelings: PropTypes.array,
};

export class ContextVsViewTime extends React.Component {
    render() {
        const viewTimesList = Object.entries(this.props.viewTime);
        const roundedViewTimes = viewTimesList.map(context =>
            [context[0] , Math.round(context[1] * 1000) / 1000]);
        return (
            <div>
                <TabularAnalysis
                    title={"Mean View Times of Different Contexts"}
                    headers={["Context","Mean View Time (seconds)"]}
                    data={roundedViewTimes}
                />
            </div>
        )
    }
}
ContextVsViewTime.propTypes = {
    viewTime: PropTypes.object,
};

export class SentimentScores extends React.Component {
    render() {
        return (
            <div>
                <SingleValueAnalysis
                    header={"Average Positivity Score"}
                    value={this.props.sentiment_average}
                    round_digits={2}
                />

                <SingleValueAnalysis
                    header={"Standard Deviation of Positivity Score"}
                    value={this.props.sentiment_std}
                    round_digits={2}
                />
            </div>
        );
    }
}
SentimentScores.propTypes = {
    sentiment_average: PropTypes.number,
    sentiment_std: PropTypes.number,
};

export class MeanReadingTimesForQuestions extends React.Component {
    render() {
        return (
            <TabularAnalysis
                title={"Mean Reading Time for Questions"}
                headers={[
                    "Question",
                    "Context",
                    "Mean time without outliers",
                    "Total number of readers",
                ]}
                data={this.props.mean_reading_times_for_questions}
            />
        );
    }
}
MeanReadingTimesForQuestions.propTypes = {
    mean_reading_times_for_questions: PropTypes.array,
};

export class RereadCountTable extends React.Component {
    render() {
        return (
            <TabularAnalysis
                title={"Mean Reread Counts for Questions and Context"}
                headers={[
                    "Question",
                    "Context",
                    "Mean Reread Counts",
                    "Total number of readers",
                ]}
                data={this.props.run_compute_reread_counts}
            />
        );
    }
}
RereadCountTable.propTypes = {
    run_compute_reread_counts: PropTypes.array,
};

export class RelevantWordPercentages extends React.Component {
    formatDataWithPercentSign(rawData) {
        //Formats the given data (usually in decimal form) as a percentage
        let formattedData = [];
        for (let [question, decimal] of rawData) {
            formattedData.push([question, `${Math.round(100 * decimal)}%`]);
        }
        return formattedData;
    }

    render() {
        return (
            <div>
                {this.props.relevantWords}
                <TabularAnalysis
                    title={"Percentage of Students Using Relevant Words"}
                    headers={[
                        "Question",
                        "Percentage",
                    ]}
                    data={this.formatDataWithPercentSign(this.props.entryData)}
                />
            </div>
        );
    }
}
RelevantWordPercentages.propTypes = {
    entryData: PropTypes.array,
    relevantWords: PropTypes.array,
};

export class PrototypeAnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // we initialize analysis to null, so we can check in render() whether
            // we've received a response from the server yet
            analysis: null,
        };
    }

    /**
     * This function is fired once this component has loaded into the DOM.
     * We send a request to the backend for the analysis data.
     */
    async componentDidMount() {
        try {
            const response = await fetch('/api_proto/analysis/');
            const analysis = await response.json();
            this.setState({analysis});
        } catch (e) {
            // For now, just log errors to the console.
            console.log(e);
        }
    }

    render() {
        if (this.state.analysis !== null) {
            const {  // object destructuring:
                total_view_time,
                run_mean_reading_analysis_for_questions,
                frequency_feelings,
                context_vs_read_time,
                question_sentiment_analysis,
                compute_median_view_time,
                run_compute_reread_counts,
                compute_mean_response_length,
                percent_using_relevant_words_by_question
            } = this.state.analysis;
            return (
                <div className={"container"}>
                    <nav className={"navbar navbar-expand-lg"}>
                        <div className={"navbar-nav"}>
                            <a
                                className={"nav-link nav-item text-dark font-weight-bold"}
                                href={"#"}
                            >Overview</a>
                            <a
                                className={"nav-link nav-item text-dark font-weight-bold"}
                                href={"#"}
                            >Analysis</a>
                        </div>
                    </nav>
                    <h1
                        className={"text-center display-4 mb-4"}
                        id={"page-title"}
                    >Analysis of Student Responses</h1>
                    <SingleValueAnalysis
                        header={"Total view time"}
                        value={total_view_time}
                        unit={"seconds"}
                    />
                    <SingleValueAnalysis
                        header={"Median view time"}
                        value={compute_median_view_time}
                        unit={"seconds"}
                    />
                    <SingleValueAnalysis
                        header={"Mean response length"}
                        value={compute_mean_response_length}
                        unit={"characters"}
                    />
                    <SentimentScores
                        sentiment_average={question_sentiment_analysis[0]}
                        sentiment_std={question_sentiment_analysis[1]}
                    />
                    <MeanReadingTimesForQuestions
                        mean_reading_times_for_questions={run_mean_reading_analysis_for_questions}
                    />
                    <RereadCountTable
                        run_compute_reread_counts={run_compute_reread_counts}
                    />
                    <FrequencyFeelingTable feelings={frequency_feelings}/>
                    <ContextVsViewTime viewTime={context_vs_read_time}/>
                    <RelevantWordPercentages
                        entryData={percent_using_relevant_words_by_question}
                    />
                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }
    }
}
