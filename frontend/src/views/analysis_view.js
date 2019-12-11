import React from "react";
import {SingleValueAnalysis, TabularAnalysis} from "../prototype/analysis_view";
import PropTypes from 'prop-types';
import Promise from "promise";

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
            current_document: this.documents[0],
            segment_num: 1,
        };
        this.handleSegmentChange = this.handleSegmentChange.bind(this);
        this.handleDocumentChange = this.handleDocumentChange.bind(this);
    }

    handleSegmentChange(event) {
        this.setState({segment_num: event.target.value});
    }

    handleDocumentChange(event) {
        this.setState({current_document: event.target.value});
    }

    render() {
        const current_segment_data = this.props.data[this.state.current_document + " " +
        this.state.segment_num];

        let max_ranges = current_segment_data["reading"];
        if (Object.keys(current_segment_data["reading"]).length <
            Object.keys(current_segment_data["rereading"]).length) {
            max_ranges = current_segment_data["rereading"];
        }
        const scroll_ranges = Object.keys(max_ranges);
        scroll_ranges.sort(scroll_range_sort);

        const num_segments = Object.keys(this.props.data).length;
        let range = n => Array.from(Array(n).keys());
        let indices = range(num_segments+1).slice(1);

        return (
            <div>
                <h3 className={"mt-4"}>
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
                Segment Number: &nbsp;
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
                <table className={"table analysis-table"}>
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
                    text = {this.props.segments[this.state.segment_num - 1].text}
                    segmentNum={1}
                />
            </div>
        )
    }
}

HeatMapAnalysis.propTypes = {
    data: PropTypes.object,
    segments: PropTypes.array,
};

class HeatMapSegment extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            readType: "reading"
        };
        this.handleReadingChange = this.handleReadingChange.bind(this);
    }

    handleReadingChange(event) {
        this.setState({readType: event.target.value});
    }

    render() {
        const segment_lines = this.props.text.split("\r\n");
        const heat_data = this.props.heatMap[this.state.readType];
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
        const scroll_ranges = Object.keys(heat_data);
        scroll_ranges.sort(scroll_range_sort);
        const max_scroll_range = scroll_ranges[scroll_ranges.length - 1];
        return (
            <div>
                This is the heat map for: &nbsp;
                <select
                    value={this.state.readType}
                    className={"segment-selector"}
                    onChange={(e) => this.handleReadingChange(e)}
                >
                    <option value={"reading"}>reading</option>
                    <option value={"rereading"}>rereading</option>
                </select>
                <div
                    className="segment"
                >
                    {segment_lines.map(
                        (line, k) => (<p className={"segment-text text-justify"} key={k}>{line}</p>)
                    )}
                    {heat_map.map((heat, i) => {
                        return (
                            <div
                                style={{
                                    position: "absolute",
                                    height: heat.range === max_scroll_range ? "500px" : "500px",
                                    width: "593px",
                                    top: heat.start + "px",
                                    backgroundColor: "rgba(255, 0, 0," + heat.percentage + ")",
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
            // Uses Promise to do multiple fetches at once
            Promise.all([
                fetch('/api/analysis/'),
                fetch('/api/documents/1/')
            ])
                .then(([res1, res2]) => Promise.all([res1.json(), res2.json()]))
                .then(([analysis, document]) => this.setState({
                    analysis,
                    document
                }));
        } catch (e) {
            // For now, just log errors to the console.
            console.log(e);
        }
    }

    render() {
        if (this.state.analysis === null) {
            return (
                <div>Loading!</div>
            );
        }

        const { // object destructuring:
            total_and_median_view_time,
            mean_reading_vs_rereading_time,
            get_number_of_unique_students,
            get_all_heat_maps,
            all_responses,
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
                <HeatMapAnalysis
                    data = {get_all_heat_maps}
                    segments={this.state.document.segments}
                />
                <TabularAnalysis
                    title="All Student Responses"
                    headers={["Segment Number", "Question Number", "Question Text", "Response"]}
                    data={all_responses}
                />
            </div>
        );
    }
}
