import React from "react";
// import PropTypes from 'prop-types';

class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 72,
            // MAKE SURE TO CHANGE THIS BACK TO 0
            // MAKE SURE TO CHANGE THIS BACK TO 0
            // MAKE SURE TO CHANGE THIS BACK TO 0
            // MAKE SURE TO CHANGE THIS BACK TO 0
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
        const data = this.state.document;

        if (data) {
            const current_segment = data.segments[this.state.segmentNum];
            const segment_text = current_segment.text;
            const segment_lines = segment_text.split("\r\n");
            const segment_questions = current_segment.questions;
            const segment_contexts = current_segment.contexts;

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{data.title}</h1>
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
                                <p>
                                    {segment_contexts.map((el,i) =>
                                        <ul key={i}>
                                            <li>{el.text}</li>
                                        </ul>)}
                                </p>
                                <p><b>Questions: </b></p>
                                <p>
                                    {segment_questions.map((el,i) =>
                                        <ul key={i}>
                                            <li>{el.text}</li>
                                        </ul>
                                    )}
                                </p>
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
