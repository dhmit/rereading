import React from "react";
import PropTypes from 'prop-types';

class SegmentQuestion extends React.Component {

    render() {
        const question_text = this.props.question.text;
        // const question_word_limit = this.props.question.response_word_limit;
        const context_text = this.props.context.text;
        return (
            <div>
                <h4>Context:</h4>
                <div className='segment-context-text'>
                    {context_text}
                </div>
                <h4>Question:</h4>
                <div className='segment-question-text'>
                    {question_text}
                </div>
                <form onSubmit={(e) => this.props.onSubmit(e)}>
                    <label><h4>Response:</h4></label>
                    <input
                        type='text'
                        value={this.props.response}
                        onChange={(e) => this.props.onChange(e)}
                    />
                    <input type='submit' value='Submit' />
                </form>

            </div>
        );
    }
}
SegmentQuestion.propTypes = {
    question: PropTypes.object,
    context: PropTypes.object,
    onChange: PropTypes.func,
    onSubmit: PropTypes.func,
    response: PropTypes.string,
};

class GlobalQuestion extends React.Component {

    render() {
        const question_text_1 = this.props.question_one.text;
        const question_text_2 = this.props.question_two.text;

        return (
            <div>
                <h4>Question 1:</h4>
                <div className='global-question-text'>
                    {question_text_1}
                </div>
                <form onSubmit={(e) => this.props.onSubmit(e)}>
                    <label><h4>Response:</h4></label>
                    <input
                        type='text'
                        value={this.props.response}
                        onChange={(e) => this.props.onChange(e)}
                    />
                    <input type='submit' value='Submit' />
                </form>
                <h4>Question 2:</h4>
                <div className='global-question-text'>
                    {question_text_2}
                </div>
                <form onSubmit={(e) => this.props.onSubmit(e)}>
                    <label><h4>Response:</h4></label>
                    <input
                        type='text'
                        value={this.props.response}
                        onChange={(e) => this.props.onChange(e)}
                    />
                    <input type='submit' value='Submit' />
                </form>

            </div>
        );
    }
}
GlobalQuestion.propTypes = {
    question_one: PropTypes.object,
    question_two: PropTypes.object,
    onChange: PropTypes.func,
    onSubmit: PropTypes.func,
    response: PropTypes.string,
};

class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 0,
            rereading: false,  // we alternate reading and rereading
            document: null,
            segmentQuestionNum: 0,
            segmentContextNum: 0,
            segmentResponseArray: [[]],
        };

        this.handleSegmentResponseChange = this.handleSegmentResponseChange.bind(this);
        this.handleSegmentResponseSubmit = this.handleSegmentResponseSubmit.bind(this);
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
            this.setState({
                segmentNum: this.state.segmentNum-1,
                rereading: true,
                segmentQuestionNum: 0,
                segmentContextNum: 0,
            });
        }
    }

    nextSegment () {
        const length = this.state.document.segments.length;
        const current_segment = this.state.segmentNum;
        if (current_segment < length){
            if (this.state.rereading) {

                // Copy the response array to prevent weird shenanigans
                const segmentResponseArray = this.state.segmentResponseArray.slice();

                const segment_questions = this.state.document.segments[current_segment].questions;
                const num_segment_questions = segment_questions.length;
                segmentResponseArray.push(Array(num_segment_questions));

                // If we're already rereading, move to the next segment
                this.setState({
                    rereading: false,
                    segmentNum: this.state.segmentNum+1,
                    segmentQuestionNum: 0,
                    segmentContextNum: 0,
                    segmentResponseArray,
                });
            } else {
                // Otherwise, move on to the rereading layout
                this.setState({rereading: true});
            }
        }
    }

    /**
     * Allows the user to change their response to a segment question
     */
    handleSegmentResponseChange(event, question_id) {
        const segmentResponseArray = this.state.segmentResponseArray.slice();

        // The index of the response into the segment is the same as its id
        segmentResponseArray[this.state.segmentNum][question_id] = event.target.value;

        this.setState({segmentResponseArray});
    }

    /**
     * Handles data when a user is trying to submit a response to a question
     */
    handleSegmentResponseSubmit(event) {
        event.preventDefault();
        console.log(this.state.segmentResponseArray[0][0]);

    }


    render() {
        const data = this.state.document;

        if (data) {
            const current_segment = data.segments[this.state.segmentNum];
            const segment_text = current_segment.text;
            const segment_lines = segment_text.split("\r\n");
            const segment_questions = current_segment.questions;
            const segment_contexts = current_segment.contexts;
            const current_global_questions = data.questions;
            const current_global_question_1 = data.questions[0];
            const current_global_question_2 = data.questions[1];

            // Generate response fields for each of the questions
            const response_fields = segment_questions.map((question, id) => {
                return (
                    <SegmentQuestion
                        question={question}
                        context={segment_contexts[this.state.segmentContextNum]}
                        onChange={this.handleSegmentResponseChange}
                        onSubmit={this.handleSegmentResponseSubmit}
                        response={this.state.segmentResponseArray[this.state.segmentNum][id]}
                        key={id}
                    />
                )
            });
            const response_fields_global = current_global_questions.map((question, id) => {
                return (
                    <GlobalQuestion
                        question_one={current_global_question_1}
                        question_two = {current_global_question_2}
                        onChange={this.handleSegmentResponseChange}
                        onSubmit={this.handleSegmentResponseSubmit}
                        response={this.state.segmentResponseArray[this.state.segmentNum][id]}
                        key={id}
                    />
                )
            });
            /*const response_fields_global_2 = current_global_question_2.map((question, id) => {
                return (
                    <GlobalQuestion
                        question_two={question}
                        onChange={this.handleSegmentResponseChange}
                        onSubmit={this.handleSegmentResponseSubmit}
                        response={this.state.segmentResponseArray[this.state.segmentNum][id]}
                        key={id}
                    />
                )
            });*/

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
                                {response_fields}
                            </div>
                        }
                        {this.state.rereading &&
                            <div className={"analysis col-4"}>
                                {response_fields_global}
                            </div>
                        }
                        {/*{this.state.rereading &&
                            <div className={"analysis col-4"}>
                                {response_fields_global_2}
                            </div>
                        }*/}
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
