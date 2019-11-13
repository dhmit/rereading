import React from "react";
import PropTypes from 'prop-types';

import {getCookie, TimeIt} from "../common";
import './reading_view.css';


/*
 * Represents the actual Segment window
 */
class Segment extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const segment_lines = this.props.text.split("\r\n");
        return (
            <div
                className="segment my-3"
                ref={this.props.segment_ref}
                onScroll={this.props.handleScroll}
            >
                {segment_lines.map(
                    (line, k) => (<p key={k}>{line}</p>)
                )}
            </div>
        );
    }
}
Segment.propTypes = {
    text: PropTypes.string,
    handleScroll: PropTypes.func,
    segment_ref: PropTypes.shape({current: PropTypes.instanceOf(Element)})
};


class OverviewWindow extends React.Component {
    render() {
        return (
            <div className={"row"}>
                <div className={"col-8"}>
                    <div className="scroll_overview">
                        {this.props.all_segments.map((el, i) => (
                            <p key={i}>{el.text}</p>)
                        )}
                    </div>
                </div>
                <div className={"col-4"}>
                    <p><b>Document Questions</b></p>
                    {this.props.document_questions.map((el, i) => (
                        <p key={i}>{el.is_overview_question ? null : el.text}</p>)
                    )}
                    <p><b>Overview Questions</b></p>
                    {this.props.document_questions.map((el, i) => (
                        <p key={i}>{el.is_overview_question ? el.text : null}</p>)
                    )}
                </div>
            </div>
        );
    }
}
OverviewWindow.propTypes = {
    all_segments: PropTypes.array,
    document_questions: PropTypes.array,
};


class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 0,
            timer: null,
            scroll_top: 0,
            scroll_data: [],
            rereading: false,  // we alternate reading and rereading
            document: null,
            interval_timer: null,
            segmentQuestionNum: 0,
            segmentContextNum: 0,
            segmentResponseArray: [],
            student_id: 15, //temporary
        };
        this.csrftoken = getCookie('csrftoken');

        this.segment_ref = React.createRef();
        this.handleSegmentResponseChange = this.handleSegmentResponseChange.bind(this);
        this.handleSegmentResponseSubmit = this.handleSegmentResponseSubmit.bind(this);
    }

    /**
     * segment_data is an array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with new segment data every time the buttons are clicked
     */
    sendData(firstTime){
        if (!firstTime && this.state.rereading) {
            const time = this.state.timer.stop();
            this.setState({scroll_data: []});
            const url = '/api/add-response/';
            const reading_data = {
                document_id: this.state.document.id,
                student_id: this.state.student_id,
                segment_responses: this.state.segmentResponseArray,
                segment_data: [{
                    id: this.state.document.segments[this.state.segment_num].id,
                    scroll_data: JSON.stringify(this.state.scroll_data),
                    view_time: time,
                    is_rereading: this.state.rereading,
                }],
            };
            console.log(JSON.stringify(reading_data));
            fetch(url, {
                method: 'POST',
                body: JSON.stringify(reading_data),
                headers: {
                    'Content-type': 'application/json',
                    'X-CSRFToken': this.csrftoken,
                }

            }).then(res => res.json()).then(response => console.log(JSON.stringify(response)))
                .catch(err => console.log(err));
        }
        const timer = new TimeIt();
        this.setState({timer});
    }


    prevSegment () {
        this.updateData(false);
        this.setState({segment_num: this.state.segment_num-1});
        this.segment_ref.current.scrollTo(0,0);
    }

    nextSegment () {
        this.updateData(false);
        if (this.state.rereading) {
            // If we're already rereading, move to the next segment
            this.setState({rereading: false, segment_num: this.state.segment_num+1});
        } else {
            // Otherwise, move on to the rereading layout
            this.setState({rereading: true});
        }
        this.segment_ref.current.scrollTo(0,0);
    }

    recordScroll() {
        const scroll_data = this.state.scroll_data;
        scroll_data.push(this.state.scroll_top);
        //
        this.setState({scroll_data});
    }

    handleScroll(e) {
        const scroll_top = e.target.scrollTop;
        this.setState({scroll_top});
    }

    toOverview () {
        this.setState({overview: true})
    }

    async componentDidMount() {
        try {
            // Hard code the document we know exists for now -- generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            const interval_timer = setInterval(() => this.recordScroll(), 2000);
            this.setState({document, interval_timer});
            this.sendData(true);
        } catch (e) {
            console.log(e);
        }
    }

    /**
     * Allows the user to change their response to a segment question
     */
    handleSegmentResponseChange(question_id, event) {
        const segmentResponseArray = this.state.segmentResponseArray.slice();

        let question_entry = null;
        for (let el of segmentResponseArray) {
            if (el.id === question_id) {
                question_entry = el;
                break;
            }
        }

        if (question_entry === null) {
            question_entry = {id: question_id};
            segmentResponseArray.push(question_entry);
        }

        question_entry.response = event.target.value;

        this.setState({segmentResponseArray});
    }

    prevSegment () {
        this.sendData(false);
        if (this.state.segment_num > 0) {
            this.setState({
                segment_num: this.state.segment_num - 1,
                rereading: true,
                segmentQuestionNum: 0,
                segmentContextNum: 0,
            });
        }
        this.segment_ref.current.scrollTo(0,0);
    }

    nextSegment () {
        this.sendData(false);
        const length = this.state.document.segments.length;
        const current_segment = this.state.segment_num;
        if (current_segment < length){
            if (this.state.rereading) {
                // If we're already rereading, move to the next segment
                this.setState({
                    rereading: false,
                    segment_num: this.state.segment_num + 1,
                    segmentQuestionNum: 0,
                    segmentContextNum: 0,
                    segmentResponseArray: [],
                });
            } else {
                // Otherwise, move on to the rereading layout
                this.setState({rereading: true});
            }
        }

        this.segment_ref.current.scrollTo(0,0);
    }

    /**
     * Handles data when a user is trying to submit a response to a question
     */
    handleSegmentResponseSubmit(event) {
        event.preventDefault();
    }

    buildQuestionFields(questions, context_text) {
        return questions.map((question, id) => (
            <React.Fragment key={id}>
                <div>
                    <h4>Context:</h4>
                    <div className='segment-context-text'>
                        {context_text}
                    </div>
                    <h4>Question:</h4>
                    <div className='segment-question-text'>
                        {question.text}
                    </div>

                    <label><h4>Response:</h4></label>
                    <input
                        type='text'
                        onChange={
                            this.handleSegmentResponseChange.bind(this, question.id)
                        }
                    />

                </div>
            </React.Fragment>
        ))
    }

    render() {
        const doc = this.state.document;
        if (!doc) {
            return (
                <div>Loading!</div>
            );
        }

        const current_segment = doc.segments[this.state.segment_num];
        const segment_questions = current_segment.questions;
        const segment_contexts = current_segment.contexts;
        const current_context =
            this.segmentContextNum < segment_contexts.length
                ? segment_contexts[this.segmentContextNum].text
                : 'No segment context given';

        // Generate response fields for each of the questions
        const segment_response_fields =
            this.buildQuestionFields(segment_questions, current_context);

        const document_questions = doc.questions;

        return (
            <div className={"container"}>
                <h1 className={"display-4 py-3 pr-3"}>{doc.title}</h1>

                {this.state.overview ?
                    <OverviewWindow
                        all_segments={doc.segments}
                        document_questions={document_questions}
                    />
                    :
                    <div className={"row"}>
                        <div className={'col-8'}>
                            <p>Segment Number: {this.state.segment_num + 1}</p>
                            <Segment
                                text={current_segment.text}
                                handleScroll={(e) => this.handleScroll(e)}
                            />
                            {this.state.segment_num > 0 &&
                            <button
                                className={"btn btn-outline-dark mr-2"}
                                onClick={() => this.prevSegment()}
                            >
                                Back
                            </button>
                            }
                            {this.state.segment_num < doc.segments.length - 1 ?
                                <button
                                    className={"btn btn-outline-dark"}
                                    onClick={() => this.nextSegment()}
                                >
                                    {this.state.rereading ? 'Next' : 'Reread'}
                                </button> :
                                <button
                                    className={"btn btn-outline-dark"}
                                    onClick={() => this.toOverview()}
                                >
                                    To Overview
                                </button>
                            }
                        </div>

                        {this.state.rereading &&
                            <div className={"analysis col-4"}>
                                {segment_response_fields}

                                {document_questions && (
                                    <div>
                                        <p><b>Document Questions: </b></p>
                                        {document_questions.map((el,i) =>
                                            <p key={i}>
                                                {el.is_overview_question ? null : el.text}
                                            </p>
                                        )}
                                    </div>
                                )}
                            </div>
                        }
                    </div>
                }
            </div>
        );

    }
}

export default ReadingView;
