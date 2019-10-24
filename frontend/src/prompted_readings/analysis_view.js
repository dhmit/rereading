import React from "react";
import PropTypes from 'prop-types';

export class FrequencyFeelingTable extends React.Component {
    render() {
        return (
            <div>
                <h1>Frequency Feelings</h1>
                <table border="1" cellPadding="5">
                    <tbody>
                        <tr>
                            <th>Word</th>
                            <th>Frequency</th>
                        </tr>
                        {this.props.feelings.map((el, i) => (
                            <tr key={i}>
                                <td>{el[0]}</td><td>{el[1]}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        )
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
                <h1>Mean View Times of Different Contexts</h1>
                <table border="1" cellPadding="5">
                    <tbody>
                        <tr>
                            <th>Context</th>
                            <th>Mean View Time (seconds)</th>
                        </tr>
                        {roundedViewTimes.map((context, i) => (
                            <tr key={i}>
                                <td>{context[0]}</td>
                                <td>{context[1]}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        )
    }
}
ContextVsViewTime.propTypes = {
    viewTime: PropTypes.object,
};



// start of reread counts

export class RereadCountsAnalysis extends React.Component {
    render() {
        const get_reread_counts = Object.entries(this.props.reread_counts);
        return (
            <div>
                <h1>Analysis of Reread Counts</h1>
                <table border="1" cellPadding="5">
                    <tbody>
                        <tr>
                            <th>0</th>
                            <th>1</th>
                            <th>2</th>
                            <th>3</th>
                            <th>4</th>
                            <th>5</th>
                            <th>6</th>
                        </tr>
                        <tr>
                            <th>{self.context[0]}</th>
                            <td>{get_reread_counts()[self.questions[0]][self.contexts[0]][0]}</td>
                            <td>{get_reread_counts()[self.questions[0]][self.contexts[0]][1]}</td>
                            <td>{get_reread_counts()[self.questions[0]][self.contexts[0]][2]}</td>
                            <td>{get_reread_counts()[self.questions[0]][self.contexts[0]][3]}</td>
                            <td>{get_reread_counts()[self.questions[0]][self.contexts[0]][4]}</td>
                            <td>{get_reread_counts()[self.questions[0]][self.contexts[0]][5]}</td>
                            <td>{get_reread_counts()[self.questions[0]][self.contexts[0]][6]}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        )
    }
}
RereadCountsAnalysis.propTypes = {
    reread_counts: PropTypes.object,
};



export class SentimentScores extends React.Component {
    render() {
        return (
            <div>
                <h3>Average Sentiment Among Students</h3>
                <h5>Positivity Score:</h5>
                <p>{this.props.sentiment_average}</p>
                <h5>Standard Deviation:</h5>
                <p>{this.props.sentiment_std}</p>
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
            <div>
                {this.props.mean_reading_times_for_questions.map((i,k) =>
                    <p key = {k}>
                            Question: {i[0]} Context: {i[1]} Mean time without outliers: {i[2]}
                            Total number of readers: {i[3]}
                    </p>
                )}
            </div>
        );
    }
}
MeanReadingTimesForQuestions.propTypes = {
    mean_reading_times_for_questions: PropTypes.array,
};

export class AnalysisView extends React.Component {
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
            const response = await fetch('/api/analysis/');
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
                        className={"text-center display-4"}
                        id={"page-title"}
                    >Analysis of Student Responses</h1>
                    <h1>Total view time</h1>
                    <p>Total view time: {total_view_time} seconds</p>
                    <h3>Mean Reading Time for Questions</h3>
                    <MeanReadingTimesForQuestions
                        mean_reading_times_for_questions={run_mean_reading_analysis_for_questions}
                    />
                    <h1>Median View Time</h1>
                    <p>Median view time: {compute_median_view_time} seconds</p>
                    <FrequencyFeelingTable feelings={frequency_feelings}/>
                    <br/>
                    <ContextVsViewTime viewTime={context_vs_read_time}/>
                    <br/>
                    <SentimentScores
                        sentiment_average={question_sentiment_analysis[0]}
                        sentiment_std={question_sentiment_analysis[1]}
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

/*



*    renderTableHeader() {
      let header = Object.keys(this.state.students[0])
      return header.map((key, index) => {
         return <th key={index}>{key.toUpperCase()}</th>
      })
   }

   render() {
      return (
         <div>
            <h1 id='title'>React Dynamic Table</h1>
            <table id='students'>
               <tbody>
                  <tr>{this.renderTableHeader()}</tr>
                  {this.renderTableData()}
               </tbody>
            </table>
         </div>
      )
   }
*
* */


export default AnalysisView;
