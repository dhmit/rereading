import React from "react";
import PropTypes from 'prop-types';

class FrequencyFeelingTable extends React.Component {
    render() {
        return (
            <div>
                <h1>Frequency Feelings</h1>
                <table border="1">
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

class ContextVsViewTime extends React.Component {
    render() {
        const viewTimesList = Object.entries(this.props.viewTime);
        const roundedViewTimes = viewTimesList.map(context =>
            [context[0] , Math.round(context[1] * 1000) / 1000]);
        return (
            <div>
                <h1>Mean View Times of Different Contexts</h1>
                <table border="1">
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
                </table>
            </div>
        )
    }
}

ContextVsViewTime.propTypes = {
    viewTime: PropTypes.object,
};

class AnalysisView extends React.Component {
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
                frequency_feelings,
                context_vs_read_time,
                compute_median_view_time,
            } = this.state.analysis;

            return (
                <div>
                    <h1>Analysis of Student Responses</h1>
                    <h3>Total view time</h3>
                    <p>{total_view_time} seconds</p>
                    <FrequencyFeelingTable feelings={frequency_feelings}/>
                    <ContextVsViewTime viewTime={context_vs_read_time}/>
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
