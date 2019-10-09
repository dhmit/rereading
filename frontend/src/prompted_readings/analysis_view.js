import React from "react";
import PropTypes from 'prop-types';

class FrequencyFeelingTable extends React.Component {
    constructor(props) {
        super(props)
        this.state = {}
    }

    render() {
        const feelings = this.props.feelings;
        return (
            <table border="1">
                <tbody>
                    <tr>
                        <th>Word</th>
                        <th>Frequency</th>
                    </tr>
                    {feelings.map((el, i) => <tr key={i}><td>{el[0]}</td><td>{el[1]}</td></tr>)}
                </tbody>
            </table>
        )
    }
}
/*
This is propTypes, which is used to verify the datatype of a certain variable
In this case, I am verifying that the variable "feelings" in the FrequencyFeelingTable component
is an array so I can use the map function on it.
 */
FrequencyFeelingTable.propTypes = {
    feelings: PropTypes.array,
}

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
                frequency_feelings,
            } = this.state.analysis;

            return (
                <div>
                    <h1>Analysis of Student Responses</h1>
                    <h3>Total view time</h3>
                    <p>{total_view_time} seconds</p>
                    <h1>Frequency Feelings</h1>
                    <FrequencyFeelingTable feelings={frequency_feelings}/>
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
