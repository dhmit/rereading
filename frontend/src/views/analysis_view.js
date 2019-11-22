import React from "react";
import {SingleValueAnalysis} from "../prototype/analysis_view";
// import PropTypes from 'prop-types';


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
        if (this.state.analysis === null) {
            return (
                <div>Loading!</div>
            );
        }

        const { // object destructuring:
            total_and_median_view_time,
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
                    value={total_and_median_view_time[0]}
                    unit={"seconds"}
                />
                <SingleValueAnalysis
                    header={"Median view time"}
                    value={total_and_median_view_time[1]}
                    unit={"seconds"}
                />
            </div>
        );
    }
}
