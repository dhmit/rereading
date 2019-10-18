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
                compute_median_view_time,
                compute_mean_response_length,
                percent_students_using_relevant_words_in_ad_context,
                percent_students_using_relevant_words_in_story_context
            } = this.state.analysis;

            return (
                <div>
                    <h1>Analysis of Student Responses</h1>
                    <h3>Total view time</h3>
                    <p>{total_view_time} seconds</p>
                    <p>{compute_median_view_time} seconds</p>
                    <p>{compute_mean_response_length}</p>
                    <h3>Students Using relevant words in ad context</h3>
                    <p>{Math.round(
                        percent_students_using_relevant_words_in_ad_context * 100)}%</p>
                    <h3>Students Using relevant words in short story context</h3>
                    <p>{Math.round(
                        percent_students_using_relevant_words_in_story_context * 100)}%</p>
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
