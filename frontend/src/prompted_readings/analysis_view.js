import React from "react";

class AnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // we initialize analysis to null, so we can check in render() whether
            // we've received a response from the server yet
            analysis: null,
        }
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
                compute_median_view_time,
            } = this.state.analysis;
            //console.log(run_mean_reading_analysis_for_questions)
            return (
                <div>
                    <h1>Analysis of Student Responses</h1>
                    <h3>Total view time</h3>
                    <p>{total_view_time} seconds</p>
                    <h3>Mean Reading Time for Questions</h3>
                    {run_mean_reading_analysis_for_questions.map((i,k) =>
                        <p key = {k}>{i}</p>
                    )}
                    <p>{compute_median_view_time}</p>
                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }
    }
}

export default AnalysisView;
