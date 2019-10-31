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
                __len__,
                __str__,
            } = this.state.document;
            return (
                <div>
                    <p>Analysis of Recitatif</p>
                    <p>{__len__}</p>
                    <p>{__str__}</p>

                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }
    }
}
