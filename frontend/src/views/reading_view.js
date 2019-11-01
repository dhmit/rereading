import React from "react";
// import PropTypes from 'prop-types';

class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 0,
            rereading: false,  // we alternate reading and rereading
            document: null,
        }
    }

    async componentDidMount() {
        try {
            // Hardcode the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            this.setState({document});
        } catch (e) {
            console.log(e);
        }

    }

    prevSegment () {
        // document will be replaced by actual data
        if (this.state.segmentNum > 0){
            this.setState({segmentNum: this.state.segmentNum-1, rereading: true});
        }
    }

    nextSegment () {
        const length = this.state.document.segments.length;
        if (this.state.segmentNum < length){
            if (this.state.rereading) {
                // If we're already rereading, move to the next segment
                this.setState({rereading: false, segmentNum: this.state.segmentNum+1});
            } else {
                // Otherwise, move on to the rereading layout
                this.setState({rereading: true});
            }
        }
    }


    render() {
        const doc = this.state.document;

        if (doc) {
            const current_segment = doc.segments[this.state.segmentNum];
            const segment_text = current_segment.text;
            const segment_lines = segment_text.split("\r\n");
            const segment_questions = current_segment.questions;
            const segment_contexts = current_segment.contexts;
            const document_questions = doc.document_questions;

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{doc.title}</h1>
                    <div className={"row"}>
                        <div className={"col-8"}>
                            <p>Segment Number: {this.state.segmentNum + 1}</p>
                            {segment_lines.map((line, k) => (
                                <p key={k}>{line}</p>)
                            )}
                            <button
                                className={"btn btn-outline-dark mr-2"}
                                onClick = {() => this.prevSegment()}
                            >
                                Back
                            </button>
                            <button
                                className={"btn btn-outline-dark"}
                                onClick = {() => this.nextSegment()}
                            >
                                {this.state.rereading ? 'Next' : 'Reread'}
                            </button>
                        </div>

                        {this.state.rereading &&
                            <div className={"analysis col-4"}>
                                <p><b>Context: </b></p>
                                {segment_contexts.map((el,i) =>
                                    <ul key={i}>
                                        <li>{el.text}</li>
                                    </ul>)}
                                <p><b>Questions: </b></p>
                                {segment_questions.map((el,i) =>
                                    <ul key={i}>
                                        <li>{el.text}</li>
                                    </ul>
                                )}
                                {document_questions && (
                                    <p>
                                        <p><b>Document Questions: </b></p>
                                        {document_questions.map((el,i) =>
                                            <ul key={i}>
                                                <li>{el.text}</li>
                                            </ul>
                                        )}
                                    </p>
                                )}

                                <p>
                                    <b>Add an annotation: </b><input
                                        type="text"
                                        value={this.state.value}
                                        onChange={this.handleChange}
                                    /><button>Submit</button>
                                </p>
                            </div>
                        }
                    </div>
                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }

    }
}

export default ReadingView;
