import React from "react";
import PropTypes from 'prop-types';

class SegmentQuestion extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            answer: '',
        };

        this.handleAnswerSubmit = this.handleAnswerSubmit.bind(this);
        this.handleAnswerChange = this.handleAnswerChange.bind(this);
    }

    handleAnswerChange(event) {
        this.setState({answer: event.target.value});
    }

    handleAnswerSubmit(event) {
        console.log(this.state.answer);
        event.preventDefault();
    }

    render() {
        return (
            <div>
                <h4>Context:</h4>
                <div className='segment-context-text'>
                    {this.props.context}
                </div>
                <h4>Question:</h4>
                <div className='segment-question-text'>
                    {this.props.question}
                </div>
                <form onSubmit={this.handleAnswerSubmit}>
                    <label><h4>Response:</h4></label>
                    <input
                        type='text'
                        value={this.state.answer}
                        onChange={this.handleAnswerChange}
                    />
                    <input type='submit' value='Submit' />
                </form>

            </div>
        );
    }
}
SegmentQuestion.propTypes = {
    question: PropTypes.string,
    context: PropTypes.string,
};

class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 0,
            rereading: false,  // we alternate reading and rereading
            document: null,
            questionNum: 0,
            contextNum: 0,
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
            segment_contexts[0] = "this is a test";
            segment_questions[0] = "this is a better test";

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
                                <SegmentQuestion
                                    question={segment_questions[this.state.questionNum]}
                                    context={segment_contexts[this.state.contextNum]}
                                />
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
