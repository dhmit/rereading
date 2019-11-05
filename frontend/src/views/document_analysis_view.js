import React from "react";
//import PropTypes from 'prop-types';

export class DocumentAnalysisView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            // we initialize analysis to null, so we can check in render() whether
            // we've received a response from the server yet
            document: null,
        };
    }

    /**
     * This function is fired once this component has loaded into the DOM.
     * We send a request to the backend for the analysis data.
     */
    async componentDidMount() {
        try {
            const response = await fetch('/api/document_analysis/');
            const document = await response.json();
            this.setState({document});
        } catch (e) {
            // For now, just log errors to the console.
            console.log(e);
        }
    }

    render() {
        if (this.state.document !== null) {
            const {
                total_word_count,
                title_author,
            } = this.state.document;
            return (
                <div>
                    <h3>Analysis of {title_author}</h3>
                    <p>Word count: {total_word_count}</p>

                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }
    }
}
