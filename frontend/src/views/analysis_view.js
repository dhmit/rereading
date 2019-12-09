import React from "react";
import {SingleValueAnalysis} from "../prototype/analysis_view";
import PropTypes from 'prop-types';

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
}

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

            const { // object destructuring:
                total_and_median_view_time,
                mean_reading_vs_rereading_time,
                get_number_of_unique_students,
                mean_reading_time_for_a_segment,
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
                    <TimeAnalysis
                        header={"Mean reading time for each segment"}
                        time_in_seconds={mean_reading_time_for_a_segment}
                    />
                    <SingleValueAnalysis
                        header={"Number of Unique Students"}
                        value={get_number_of_unique_students}
                        unit={"students"}
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
