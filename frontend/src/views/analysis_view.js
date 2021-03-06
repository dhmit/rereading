import React from "react";
import {
    SingleValueAnalysis,
    RelevantWordPercentages,
    TabularAnalysis,
} from "../prototype/analysis_view";
import { Footer, Spinner } from "../common";
import PropTypes from 'prop-types';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import "../index.scss";

export class RereadCountTable extends React.Component {
    render() {
        return (
            <TabularAnalysis
                title ={"Reread Counts per Segment"}
                headers={[
                    "Segment Number",
                    "Mean Reread Count",
                ]}
                data={this.props.compute_reread_counts}
            />
        );
    }
}
RereadCountTable.propTypes = {
    compute_reread_counts: PropTypes.array,
};


export class RelevantWordsByQuestions extends React.Component {
    render() {
        return (
            <TabularAnalysis
                /*
                Gives a list of the most common words in student responses for a particular
                 question, ommiting stop words such as 'is' or 'the'.
                 */
                title={"Frequency Counts for Student Response with Relevant Words"}
                subtitle={"This function counts the number of responses that respond with" +
                " the relevant words."}
                headers={[
                    "Question",
                    "Count"
                ]}
                data={this.props.relevant_words_by_question}
            />
        );
    }
}

RelevantWordsByQuestions.propTypes = {
    relevant_words_by_question: PropTypes.array,
};

export function formatTime(timeInSeconds, secondsRoundDigits) {
    /*
        Returns a string in the format "x hours y minutes z seconds".
        Any quantities equal to zero will not be included unless the total time is 0 seconds.
        If secondsRoundDigit is set, the seconds value will be rounded to that decimal place.
     */
    const SECONDS_PER_MINUTE = 60;
    const SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE;
    let remainingTime = timeInSeconds;

    let hours = Math.floor(remainingTime / SECONDS_PER_HOUR);
    remainingTime %= SECONDS_PER_HOUR;
    let minutes = Math.floor(remainingTime / SECONDS_PER_MINUTE);
    remainingTime %= SECONDS_PER_MINUTE;
    let seconds = remainingTime;

    let hoursFormat = formatPluralUnits(hours, "hour");
    let minutesFormat = formatPluralUnits(minutes, "minute");
    let secondsFormat = formatPluralUnits(seconds, "second", secondsRoundDigits);

    //Put the three units together
    let finalFormat = "";
    for (let str of [hoursFormat, minutesFormat, secondsFormat]) {
        if (str !== "") {
            finalFormat += str + " ";
        }
    }
    finalFormat = finalFormat.trim();

    if (finalFormat === "") {
        return "0 seconds";
    }

    return finalFormat;
}

function formatPluralUnits(value, singularUnit, roundDigits = undefined) {
    /*
    Formats units that can be singular or plural.
    A value of zero will return an empty string.
     */
    let roundedValue;
    if (roundDigits !== undefined) {
        roundedValue = value.toFixed(roundDigits);
    } else {
        roundedValue = value;
    }

    if (roundedValue === 0) {
        return "";
    }

    let formattedString = `${roundedValue} ${singularUnit}`;
    if (value !== 1) {
        formattedString += "s";
    }
    return formattedString;
}

export class TimeAnalysis extends React.Component {
    render() {
        return (
            <SingleValueAnalysis
                header={this.props.header}
                value={formatTime(this.props.time_in_seconds, this.props.round_digits)}
                unit=""
            />
        )
    }
}
TimeAnalysis.propTypes = {
    header: PropTypes.string,
    time_in_seconds : PropTypes.number,
    round_digits: PropTypes.number,
};

const scroll_range_sort = (a, b) => {
    const a_ranges = a.split(" — ");
    const b_ranges = b.split(" — ");
    const a_value = parseInt(a_ranges[1]);
    const b_value = parseInt(b_ranges[1]);
    return a_value - b_value;
};

/**
 * Sometimes, the backend data records some scroll ranges that go beyond the text so this is to
 * remove those inconsistencies.
 * @param scroll_ranges: a list of scroll ranges
 * @param heat_map: the heat map with scroll range as key and # seconds as value. (optional)
 */
const simplify_scroll_range = (scroll_ranges, heat_map) => {
    let prev_scroll = 0;
    const simplified_scroll_ranges = [];
    for (let i = 0; i < scroll_ranges.length; i++){
        const scroll_end = parseInt(scroll_ranges[i].split(" — ")[1]);
        if (scroll_end === prev_scroll + 500) {
            prev_scroll = scroll_end;
            simplified_scroll_ranges.push(scroll_ranges[i]);
        }
        else if (heat_map) {
            delete heat_map[scroll_ranges[i]];
        }
    }
    return simplified_scroll_ranges;
};

export class HeatMapAnalysis extends React.Component {
    constructor(props) {
        super(props);

        this.documents = [];
        const all_segments = Object.keys(this.props.data);
        for (let i = 0; i < all_segments.length; i++) {
            const document_title = all_segments[i].split(" ")[0];
            if (!this.documents.includes(document_title)) {
                this.documents.push(document_title);
            }
        }
        this.state = {
            document: null,
            current_document: this.documents[0],
            segment_num: 1,
        };

        this.handleSegmentChange = this.handleSegmentChange.bind(this);
        this.handleDocumentChange = this.handleDocumentChange.bind(this);
    }

    async componentDidMount() {
        try {
            const response = await fetch('/api/documents/1/');
            const document = await response.json();
            this.setState({document});
        } catch (e) {
            // For now, just log errors to the console.
            console.log(e);
        }
    }

    handleSegmentChange(event) {
        this.setState({segment_num: event.target.value});
    }

    handleDocumentChange(event) {
        this.setState({current_document: event.target.value});
    }

    render() {
        if (!this.state.document) {
            return (
                <div>Loading!</div>
            );
        }
        const current_segment_data =
            this.props.data[this.state.current_document + " " + this.state.segment_num];

        let max_ranges = current_segment_data["reading"];
        if (Object.keys(current_segment_data["reading"]).length <
            Object.keys(current_segment_data["rereading"]).length) {
            max_ranges = current_segment_data["rereading"];
        }
        let scroll_ranges = Object.keys(max_ranges);
        scroll_ranges.sort(scroll_range_sort);
        scroll_ranges = simplify_scroll_range(scroll_ranges);

        const num_segments = Object.keys(this.props.data).length;
        let range = n => Array.from(Array(n).keys());
        let indices = range(num_segments+1).slice(1);

        return (
            <div>
                <h3 className={"mt-4 analysis-subheader"}>
                    Heat Map for &nbsp;
                    <select
                        value={this.state.current_document}
                        className={"segment-selector"}
                        onChange={(e) => this.handleDocumentChange(e)}
                    >
                        {this.documents.map((k, entry) => {
                            return (
                                <option key={k} value={this.documents[entry]}>
                                    {this.documents[entry]}
                                </option>
                            )
                        })}
                    </select>
                </h3>
                <p>This function provides a color coded map of time spent on different sections
                    of the text. The darker the section, the more total time readers spent on it.
                    A heat map is available for both the reading and the rereading data for all
                segments of the text.</p>
                <span className={"analysis-label"}> Segment Number: &nbsp; </span>
                <select
                    value={this.state.segment_num}
                    className={"segment-selector"}
                    onChange={(e) => this.handleSegmentChange(e)}
                >
                    {indices.map((k, entry) => {
                        return (
                            <option key={k} value={indices[entry]}>
                                {indices[entry]}
                            </option>
                        )
                    })}
                </select>
                <table className={"table analysis-table mt-2"}>
                    <tbody>
                        <tr>
                            <th>Scroll Position</th>
                            <th>Reading (seconds)</th>
                            <th>Rereading (seconds)</th>
                        </tr>
                        {scroll_ranges.map( (k, range) => {
                            range = scroll_ranges[range];
                            return (
                                <tr key={k}>
                                    <th className={"p-3"}>
                                        {range}
                                    </th>
                                    <td className={"p-3"}>
                                        {current_segment_data["reading"][range]}
                                    </td>
                                    <td className={"p-3"}>
                                        {current_segment_data["rereading"][range]}
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
                <HeatMapSegment
                    heatMap = {current_segment_data}
                    text = {this.state.document.segments[this.state.segment_num - 1].text}
                    segmentNum={1}
                />
            </div>
        )
    }
}

HeatMapAnalysis.propTypes = {
    data: PropTypes.object,
};

class HeatMapSegment extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            readType: "reading",
            finalHeight: 500,
        };
        this.segment_ref = React.createRef();
        this.handleReadingChange = this.handleReadingChange.bind(this);
    }

    handleReadingChange(event) {
        this.setState({readType: event.target.value});
    }

    componentDidUpdate(prevProps, prevState, snapshot) {// eslint-disable-line no-unused-vars
        const segment_height = this.segment_ref.current.scrollHeight;
        const heat_data = this.props.heatMap[this.state.readType];
        const scroll_ranges = Object.keys(heat_data);
        scroll_ranges.sort(scroll_range_sort);
        const max_scroll_range = scroll_ranges[scroll_ranges.length - 1];
        const height = 500 - (parseInt(max_scroll_range.split(" — ")[1]) -
            segment_height);
        if (this.state.finalHeight !== height) {
            this.setState({finalHeight: height});
        }
    }

    componentDidMount() {
        this.setState({readType:"reading"});
    }

    render() {
        const segment_lines = this.props.text.split("\r\n");
        const heat_data = this.props.heatMap[this.state.readType];
        let scroll_ranges = Object.keys(heat_data);
        scroll_ranges.sort(scroll_range_sort);
        scroll_ranges = simplify_scroll_range(scroll_ranges, heat_data);
        const max_scroll_range = scroll_ranges[scroll_ranges.length - 1];

        const max_heat = Math.max(...Object.values(heat_data));
        // The intensity of the heat map is determined by the amount of seconds spent viewing that
        // section divided by the maximum time spent viewing any of the sections of that segment
        const heat_map = Object.keys(heat_data).map(range => {
            return {
                start: range.split(" — ")[0],
                percentage: 0.6 * heat_data[range] / max_heat,
                range: range,
            }
        });

        return (
            <div>
                <span className={"analysis-label"}> This is the heat map for: &nbsp; </span>
                <select
                    value={this.state.readType}
                    className={"segment-selector"}
                    onChange={(e) => this.handleReadingChange(e)}
                >
                    <option value={"reading"}>reading</option>
                    <option value={"rereading"}>rereading</option>
                </select>
                <div
                    className="heat-segment mt-2"
                    ref={this.segment_ref}
                >
                    {segment_lines.map(
                        (line, k) => (<p className={"segment-text text-justify"} key={k}>{line}</p>)
                    )}
                    {heat_map.map((heat, i) => {
                        return (
                            <div
                                style={{
                                    position: "absolute",
                                    height: heat.range === max_scroll_range ?
                                        this.state.finalHeight + "px" :
                                        "500px",
                                    width: "593px",
                                    top: heat.start + "px",
                                    backgroundColor: "rgba(255, 0, 0," + heat.percentage + ")",
                                    zIndex: 2,
                                }}
                                key={i}
                            >
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
}
HeatMapSegment.propTypes = {
    text: PropTypes.string,
    heatMap: PropTypes.object,
    segmentNum: PropTypes.number,
};

export class AllResponsesTable extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 1,
        };
        this.handleSegmentChange = this.handleSegmentChange.bind(this);
    }

    handleSegmentChange(event) {
        this.setState({segment_num: event.target.value});
    }

    render() {
        let range = n => Array.from(Array(n).keys());
        let segments = range(5);
        const dataFilteredBySegment = this.props.data.filter(
            (entry) => entry[0] === Number(this.state.segment_num)
        );

        return (
            <div>
                <h3 className={"analysis-subheader mt-4"}> {this.props.title} </h3>
                Segment Number: &nbsp;
                <select
                    value={this.state.segment_num}
                    className={"segment-selector"}
                    onChange={(e) => this.handleSegmentChange(e)}
                >
                    {segments.map((k, entry) => {
                        return (
                            <option key={k} value={segments[entry] + 1}>
                                {segments[entry] + 1}
                            </option>
                        )
                    })}
                </select>
                <table className={"table analysis-table"}>
                    <tbody>
                        <tr>
                            {/* Auto generate the headers */}
                            {this.props.headers.map((header, k) => (
                                <th className={"p-2"} key={k}>{header}</th>)
                            )}
                        </tr>
                        {dataFilteredBySegment.map((entry, k) => (
                            <tr key={k}>
                                <td className={"p-2"} key={k * 2}>
                                    {entry[1]}
                                </td>
                                <td className={"p-2"} key={k * 2 + 1}>
                                    {entry[2]}
                                </td>
                                <td>
                                    <table><tbody>
                                        {entry[3].map((tuple, k) => (
                                            <tr className={"response-tr"} key={k}>
                                                <td className={"p-2 response-td"} key={k * 2}>
                                                    {tuple[0]}
                                                </td>
                                                <td className={"p-2 response-td"} key={k * 2 + 1}>
                                                    {tuple[1].length > 0
                                                        ? tuple[1].map((evidence, k) => (
                                                            <ul key={k}>
                                                                <li>{evidence}</li>
                                                            </ul>
                                                        ))
                                                        : <p>N/A</p>
                                                    }
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody></table>
                                </td>
                            </tr>)
                        )}
                    </tbody>
                </table>
            </div>

        )
    }
}
AllResponsesTable.propTypes = {
    headers: PropTypes.array,
    data: PropTypes.array,
    title: PropTypes.string,
};

export class AnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // we initialize analysis to null, so we can check in render() whether
            // we've received a response from the server yet
            analysis: null,
            document: null,
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
        if (this.state.analysis === null) {
            return <Spinner />;
        }

        const { // object destructuring:
            total_and_median_view_time,
            mean_reading_vs_rereading_time,
            get_number_of_unique_students,
            compute_reread_counts,
            relevant_words_by_question,
            percent_using_relevant_words_by_question,
            get_all_heat_maps,
            all_responses,
            most_common_words_by_question,
            relevant_words_percent_display_question
        } = this.state.analysis;

        return (
            <>
                <div className={"container"}>
                    <h1
                        className={"text-center display-4 mb-4"}
                        id={"page-title"}
                    >Analysis of Student Responses</h1>
                    <div className={"analysis-container"}>

                        <Tabs defaultActiveKey="Time Data" className="tabs">
                            <Tab eventKey="Time Data" title="Time Data" className="tab">
                                <TimeAnalysis
                                    header={"Total view time"}
                                    time_in_seconds={total_and_median_view_time[0]}
                                />
                                <TimeAnalysis
                                    header={"Median view time"}
                                    time_in_seconds={total_and_median_view_time[1]}
                                />
                                <TimeAnalysis
                                    header={"Mean reading view time"}
                                    time_in_seconds={mean_reading_vs_rereading_time[0]}
                                />
                                <TimeAnalysis
                                    header={"Mean rereading view time"}
                                    time_in_seconds={mean_reading_vs_rereading_time[1]}
                                />
                                <SingleValueAnalysis
                                    header={"Number of Unique Students"}
                                    value={get_number_of_unique_students}
                                    unit={"students"}
                                />
                                <RereadCountTable
                                    compute_reread_counts={compute_reread_counts}
                                />
                            </Tab>
                            <Tab eventKey="Heat Map" title="Heat Map">
                                <HeatMapAnalysis
                                    data={get_all_heat_maps}
                                />
                            </Tab>
                            <Tab eventKey="Relevant Words" title="Relevant Words">
                                <TabularAnalysis
                                    title = {
                                        "Percentage and Frequency of Relevant Words per Question"
                                    }
                                    subtitle = {
                                        "The following table displays the percentage of the" +
                                        " responses that use the relevant words defined by" +
                                        " Professor Alexandre, the total number of responses" +
                                        " with at least one relevant word, and the frequencies" +
                                        " of the relevant words per question by occurrences." +
                                        "Here are the relevant words:\"stereotypes\", \"bias\", " +
                                        "\"assumptions\", \"assume\", \"narrator\", \"memory\",\n" +
                                        "\"forget\", \"Twyla\", \"Maggie\", \"Roberta\", " +
                                        "\"black\", " + "" + "\"white\", \"prejudice\",\n" +
                                        "\"mothers\", \"segregation\", \"hate\", \"hatred\", " +
                                        "\"love\", \"love-hate\",\n" +
                                        "\"remember\", \"children\", \"recall\", \"kick\", " +
                                        "\"truth\"," + " \"dance\", \"sick\",\n" +
                                        "\"fade\", \"old\", \"Mary\", \"sandy\", \"race\", " +
                                        "\"racial\", \"racism\",\n" +
                                        "\"colorblind\", \"disabled\", \"marginalized\", " +
                                        "\"poor\"," + "" + "\"rich\", \"wealthy\",\n" +
                                        "\"middle-class\", \"working-class\", \"consumers\", " +
                                        "\"shopping\", \"read\",\n" +
                                        "\"misread\", \"reread\", \"reconsider\", \"confuse\", " +
                                        "\"wrong\", \"mistaken\",\n" +
                                        "\"regret\", \"mute\", \"voiceless\", \"women\", \"age\"," +
                                        "" + "\"bird\", \"time\", \"scene\",\n" +
                                        "\"setting\", \"Hendrix \", \"universal\", \"binary\", " +
                                        "\"deconstruct\",\n" +
                                        "\"question\", \"wrong\", \"right\", \"incorrect\", " +
                                        "\"false\", \"claims\", \"true\",\n" +
                                        "\"truth\", \"unknown\", \"ambiguous\", \"unclear\""
                                    }
                                    headers={[
                                        "Question",
                                        "Percentage",
                                        "Total Number of Responses with At Least One Relevant" +
                                        " Word",
                                        "Relevant Word Frequency Per Question"
                                    ]}
                                    data={relevant_words_percent_display_question}
                                />
                                <RelevantWordPercentages
                                    words={percent_using_relevant_words_by_question[0]}
                                    entryData={percent_using_relevant_words_by_question[1]}
                                />
                                <RelevantWordsByQuestions
                                    relevant_words_by_question={relevant_words_by_question}
                                />
                            </Tab>
                            <Tab eventKey="Top Words" title="Top Words">
                                <TabularAnalysis
                                    title="Top Words by Question"
                                    subtitle={
                                        "This function finds the most common words used in "
                                        + "student responses to a specific question."
                                    }
                                    headers={[
                                        "Segment Number",
                                        "Question Number",
                                        "Question Text",
                                        "Top Words"
                                    ]}
                                    data={most_common_words_by_question}
                                />
                            </Tab>
                            <Tab eventKey="student responses" title="All Responses">
                                <AllResponsesTable
                                    title="All Student Responses"
                                    headers={[
                                        "Question Number",
                                        "Question Text",
                                        "Response and Evidence",
                                    ]}
                                    data={all_responses}
                                />
                            </Tab>
                        </Tabs>
                    </div>
                </div>

                <Footer />
            </>
        );
    }
}
