import React from "react";
import PropTypes from 'prop-types';

class CommonResponses extends React.Component {
    render() {
        return (
            <div>
                <h3>Most Common Responses</h3>
                <table>
                    <tbody>
                        <tr>
                            <th>Question</th>
                            <th>Context</th>
                            <th>Most common response(s)</th>
                        </tr>
                        {this.props.responses.map((resp_obj, i) =>
                            <tr key={i}>
                                <td>{resp_obj.question}</td>
                                <td>{resp_obj.context}</td>
                                <td>{resp_obj.answers.map(answer => ' ' + answer + ' ')}</td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        );
    }
}

CommonResponses.propTypes = {
    responses: PropTypes.array,
};

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
                all_responses,
                compute_median_view_time,
            } = this.state.analysis;

            return (
                <div>
                    <h1>Analysis of Student Responses</h1>
                    <h3>Total view time</h3>
                    <p>{total_view_time} seconds</p>
                    <CommonResponses responses={all_responses} />
                    <p>{compute_median_view_time}</p>
                    <p>Total view time: {total_view_time} seconds</p>
                    <p>Median view time: {compute_median_view_time} seconds</p>
                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }
    }
}

export { CommonResponses }
export default AnalysisView;
