import React from "react";
import PropTypes from 'prop-types';

import {getCookie, TimeIt} from "../common";

// enum representing which view to show in reading view
const VIEWS = {
    INSTRUCTIONS_NAME: 0,
    READING: 1,
    OVERVIEW: 2,
};

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
                className="segment"
                ref={this.props.segment_ref}
                onScroll={this.props.handleScroll}
                onMouseUp={this.props.handleSelectionDragEnd}
            >
                {segment_lines.map(
                    (line, k) => (<p className={"segment-text text-justify"} key={k}>{line}</p>)
                )}
            </div>
        );
    }
}
Segment.propTypes = {
    text: PropTypes.string,
    handleScroll: PropTypes.func,
    handleSelectionDragEnd: PropTypes.func,
    segment_ref: PropTypes.shape({current: PropTypes.instanceOf(Element)})
};

class Question extends React.Component {

    render(){
        const ems = this.props.evidenceModeState;
        const evidenceModeActive =
            ems.active
            && ems.question_id === this.props.question.id
            && ems.is_document_question === this.props.is_document_question;

        const evidence = this.props.response.evidence;
        const response_text = this.props.response.response;

        return(
            <div className="card mb-4">
                <div className="card-header">
                    <div className='segment-question-text question-text'>
                        {this.props.question.text}
                    </div>
                </div>
                <div className="card-body">
                    <textarea
                        className={'form-control form-control-lg questions-boxes'}
                        rows="4"
                        onChange={this.props.handleResponseChange}
                        value={response_text}
                    />
                    {this.props.question.require_evidence && (
                        <div className="evidence-section">
                            {evidence && evidence.length ?
                                <div className="evidence-values-section mt-1">
                                    <div className="evidence-values">
                                        {evidence.map((evidence_text, i) => (
                                            <div
                                                className="card card-body mb-3 evidence-value"
                                                key={i}
                                            >
                                                {'"' + evidence_text + '"'}
                                                <div className="text-right">
                                                    <button
                                                        className="remove-evidence-button"
                                                        onClick={
                                                            () => this.props.handleRemoveEvidence(
                                                                this.props.is_document_question,
                                                                this.props.question.id,
                                                                i,
                                                            )
                                                        }
                                                    >X</button>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                                :
                                ''
                            }
                            <button
                                className="evidence-toggle-button"
                                onClick={this.props.toggleAddEvidenceMode}
                            >
                                {evidenceModeActive ? 'Stop Tagging' : 'Add Evidence'}
                            </button>
                            {evidenceModeActive &&
                            <span className="form-hint-text">
                                Highlight parts of the text to save as evidence.
                            </span>
                            }
                        </div>
                    )}
                </div>
            </div>
        );
    }
}

Question.propTypes = {
    question: PropTypes.object,
    response: PropTypes.object,
    is_document_question: PropTypes.bool,
    evidenceModeState: PropTypes.object,
    handleResponseChange: PropTypes.func,
    handleRemoveEvidence: PropTypes.func,
    toggleAddEvidenceMode: PropTypes.func,
}

class NavBar extends React.Component {
    render() {
        const on_last_segment_and_rereading =
            this.props.segment_num === this.props.document_segments.length - 1
            && this.props.rereading;

        return (
            <div className="row">
                <div className="col">
                    {this.props.segment_num > 0 &&
                    <button
                        className="btn btn-outline-dark"
                        onClick={() => this.props.prevSegment()}
                    >
                        Back
                    </button>
                    }
                    {!on_last_segment_and_rereading
                        ? (
                            <button
                                className="next-btn"
                                onClick={() => this.props.nextSegment()}
                            >
                                {this.props.rereading ? 'Next' : 'Reread'}
                            </button>
                        )
                        : (
                            <button
                                className="next-btn"
                                onClick={() => this.props.toOverview()}
                            >
                                To Overview
                            </button>
                        )
                    }
                </div>
            </div>
        )
    }
}
NavBar.propTypes = {
    document_segments: PropTypes.array,
    segment_num: PropTypes.number,
    rereading: PropTypes.bool,
    prevSegment: PropTypes.func,
    nextSegment: PropTypes.func,
    toOverview: PropTypes.func,
    handleJumpToFieldKeyDown: PropTypes.func,
    handleJumpToFieldChange: PropTypes.func,
    handleJumpToButton: PropTypes.func,
    userCanJump: PropTypes.func
};

class OverviewView extends React.Component {
    render() {
        const full_document_text = [];
        this.props.all_segments.map((el) => full_document_text.push(el.text.split("\r\n")));
        const document_questions = this.props.document_questions;
        const overview_questions = this.props.overview_questions;
        const document_response_fields = this.props.buildQuestionFields(document_questions);
        const overview_response_fields = this.props.buildQuestionFields(overview_questions);

        return (
            <div className="row">
                <div className="col-8">
                    <div className="scroll-overview">
                        {full_document_text.map((segment_text_array) => (
                            segment_text_array.map((text, i) => (
                                <p key={i}>{text}</p>
                            ))
                        ))}
                    </div>
                </div>
                <div className="col-4 questions-container">
                    <p><b>Document Questions</b></p>
                    {document_response_fields}
                    <p><b>Overview Questions</b></p>
                    {overview_response_fields}
                </div>
            </div>
        );
    }
}
OverviewView.propTypes = {
    all_segments: PropTypes.array,
    document_questions: PropTypes.array,
    overview_questions: PropTypes.array,
    buildQuestionFields: PropTypes.func,
};

export class InstructionsNameView extends React.Component {
    render() {
        return (
            <div className={"container"}>
                <h1 className={"display-4 text-center mt-4"}>
                    Instructions
                </h1>
                <div className={"mb-5"}>
                    <p id={"instructions-overview"}>
                        Do a close reading of the text by following
                        these steps:
                        Read each segment of the text one segment at a time, from
                        segment 1 to segment 5, while answering
                        questions for each segment along the way.
                    </p>
                    <ol id={"instructions-list"}>
                        <li>
                            After your first reading of a segment, click the “reread”
                            button in order to access the questions for that particular
                            segment.
                        </li>
                        <li>
                            Provide an answer to each question posed for that segment,
                            including the two “common questions.”
                        </li>
                        <li>
                            After you finish answering the questions for that segment,
                            click the “next” button in order to access the next segment.
                        </li>
                        <li>
                            For each segment, highlight passages that provide evidence
                            to support your answer to common question #2.
                        </li>
                    </ol>
                </div>
                <h4>Enter your name or leave blank to remain anonymous</h4>
                <div className={"input-group"}>
                    <input
                        className={"form-control"}
                        type={"text"}
                        onChange={(e) => this.props.handleStudentName(e)}
                        required
                    />
                    <div className={"input-group-append"}>
                        <button
                            className={"btn btn-outline-dark "}
                            onClick={() => this.props.startReading()}
                        >
                            Start Reading
                        </button>
                    </div>
                </div>
            </div>
        )
    }
}
InstructionsNameView.propTypes = {
    handleStudentName: PropTypes.func,
    startReading: PropTypes.func,
};

export class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            current_view: VIEWS.INSTRUCTIONS_NAME,
            student_name: "",
            segment_num: 0,
            timer: null,
            scroll_top: 0,
            scroll_data: [],
            segments_viewed: [0],
            maximum_jump_allowed: 0,
            jump_to_value: null,
            rereading: false,  // we alternate reading and rereading
            document: null,
            reading_data: null,
            interval_timer: null,
            segmentQuestionNum: 0,
            segmentResponseArray: [],
            documentResponseArray: [],
            evidenceModeState: {
                active: false,
                question_id: 0,
                is_document_question: false,
            },
            current_selection: '',
            previousSegmentResponses: {},
        };
        this.csrftoken = getCookie('csrftoken');

        this.segment_ref = React.createRef();
        this.allQuestionsAreCompleted = this.allQuestionsAreCompleted.bind(this);
        this.prevSegment = this.prevSegment.bind(this);
        this.nextSegment = this.nextSegment.bind(this);
        this.toOverview = this.toOverview.bind(this);
        this.handleJumpToFieldChange = this.handleJumpToFieldChange.bind(this);
        this.handleJumpToButton = this.handleJumpToButton.bind(this);
        this.handleJumpToFieldKeyDown = this.handleJumpToFieldKeyDown.bind(this);
        this.userCanJump = this.userCanJump.bind(this);
        this.buildQuestionFields = this.buildQuestionFields.bind(this);
        this.startReading = this.startReading.bind(this);
        this.handleStudentName = this.handleStudentName.bind(this);
        this.toggleAddEvidenceMode = this.toggleAddEvidenceMode.bind(this);
        this.handleResponseChange.bind(this);
        this.handleRemoveEvidence.bind(this);
    }

    async startReading() {
        try {
            // Hard code the document we know exists for now -- generalize later...
            const url = '/api/documents/1/';
            const data = {
                name: this.state.student_name,
            };
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-type': 'application/json',
                    'X-CSRFToken': this.csrftoken,
                }
            });
            const response_json = await response.json();
            const document = response_json.document;
            const reading_data = response_json.reading_data;
            const interval_timer = setInterval(() => this.recordScroll(), 100000000);
            // CHANGE ME BACK!
            // CHANGE ME BACK!
            // CHANGE ME BACK!
            // CHANGE ME BACK!
            // CHANGE ME BACK!
            // CHANGE ME BACK!
            this.setState({
                document,
                interval_timer,
                reading_data,
                current_view: VIEWS.READING,
            });
            this.sendData(true);
        } catch (e) {
            console.log(e);
        }
    }

    /**
     * segment_data is an array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with new segment data every time the buttons are clicked
     */
    async sendData(firstTime){
        if (!firstTime) {
            const time = this.state.timer.stop();
            this.setState({scroll_data: []});
            const url = '/api/add-response/';
            const reading_data = {
                reading_data_id: this.state.reading_data.id,
                segment_data: [{
                    id: this.state.document.segments[this.state.segment_num].id,
                    scroll_data: JSON.stringify(this.state.scroll_data),
                    view_time: time,
                    is_rereading: this.state.rereading,
                    segment_responses: this.state.segmentResponseArray,
                }],
                document_responses: this.state.documentResponseArray,
            };
            const response = await fetch(url, {
                method: 'POST',
                body: JSON.stringify(reading_data),
                headers: {
                    'Content-type': 'application/json',
                    'X-CSRFToken': this.csrftoken,
                }
            });
            const new_reading_data = await response.json();
            this.setState({reading_data: new_reading_data});
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    recordScroll() {
        const scroll_data = this.state.scroll_data;
        scroll_data.push(this.state.scroll_top);
        this.setState({scroll_data});
    }

    handleScroll(e) {
        const scroll_top = e.target.scrollTop;
        this.setState({scroll_top});
    }


    handleResponseChange(is_document_question, question_id, event) {
        const update_dict = {
            response: event.target.value,
        };
        if (is_document_question) {
            update_dict.response_segment = this.state.segment_num;
        }
        this.updateResponseObject(is_document_question, question_id, update_dict);
    }


    getOrCreateResponseObjectAndArray(is_document_question, question_id) {
        let responseArray;
        if (is_document_question) {
            responseArray = this.state.documentResponseArray.slice();
        } else {
            responseArray = this.state.segmentResponseArray.slice();
        }

        // Try to find an existing response
        let response = null;
        for (let el of responseArray) {
            if (el.id === question_id) {
                response = el;
                break;
            }
        }

        // Add a new response object if there isn't one already
        if (response === null) {
            response = {id: question_id};
            responseArray.push(response);
        }

        return [response, responseArray];
    }

    /**
     * Allows the user to change their response to a question
     */
    updateResponseObject(is_document_question, question_id, update_dict) {
        const [response, responseArray] =
            this.getOrCreateResponseObjectAndArray(is_document_question, question_id);

        // Update values in response object with update_dict
        Object.assign(response, update_dict);

        if (is_document_question) {
            this.setState({documentResponseArray: responseArray});
        } else {
            this.setState({segmentResponseArray: responseArray});
        }
    }

    allQuestionsAreCompleted () {
        const doc = this.state.document;
        const current_segment = doc.segments[this.state.segment_num];
        const segment_questions = current_segment.questions;
        const document_questions = doc.document_questions;
        const document_responses = this.state.documentResponseArray;
        const segment_responses = this.state.segmentResponseArray;

        if (document_responses.length === document_questions.length &&
            segment_responses.length === segment_questions.length) {
            for (let element of document_responses) {
                if (element.response.trim() === ""){
                    return false;
                }
            }
            for (let element of segment_responses) {
                if (element.response.trim() === ""){
                    return false;
                }
            }
        }
        else
        {
            return false;
        }

        return true;
    }

    prevSegment () {
        this.gotoSegment(this.state.segment_num - 1);
    }

    nextSegment () {
        if (this.state.rereading) {
            // If we're already rereading, move to the next segment
            this.gotoSegment(this.state.segment_num + 1);
        } else {
            // Otherwise, move on to the rereading layout
            this.sendData(false);
            this.setState({rereading: true});
        }
    }

    gotoSegment(segmentNum) {
        this.sendData(false);

        let segmentCount = this.state.document.segments.length;
        let segment_num = this.state.segment_num;

        if (!this.allQuestionsAreCompleted()) {
            //Make sure the user can't jump past the current segment if they haven't completed
            // all questions
            this.setState({maximum_jump_allowed: segment_num});
            if (segmentNum > segment_num) {
                alert("Please respond to every question before moving on.");
                return;
            }
        }

        if (segmentNum >= 0 && segmentNum < segmentCount) {

            const segments_viewed = this.state.segments_viewed.slice();
            let rereading = segments_viewed.includes(segmentNum);
            //The segment number is pushed regardless of whether or not the user has read the page
            // before so that page reread order can also be determined.
            segments_viewed.push(segmentNum);
            // Store the current segment reading data into state
            const previousSegmentResponses = this.state.previousSegmentResponses;
            previousSegmentResponses[this.state.segment_num] = this.state.segmentResponseArray;
            const segmentResponseArray = segmentNum in previousSegmentResponses ?
                previousSegmentResponses[segmentNum] : [];

            let maximum_jump_allowed = this.state.maximum_jump_allowed;
            if (segmentNum > maximum_jump_allowed) {
                maximum_jump_allowed = segmentNum;
            }

            this.setState({
                rereading,
                segments_viewed,
                segment_num: segmentNum,
                segmentQuestionNum: 0,
                segmentResponseArray,
                previousSegmentResponses,
                maximum_jump_allowed
            });
            this.segment_ref.current.scrollTo(0,0);
        }
    }

    handleJumpToFieldKeyDown = (e) => {
        if (e.key === 'Enter') {
            this.handleJumpToButton(); //The enter key should be treated the same the jump button
        }
    };

    handleJumpToFieldChange = (e) => {
        let numericValue = parseInt(e.target.value) - 1;
        this.setState({jump_to_value: numericValue});
    };

    userCanJump = () => {
        let jump_to_value = this.state.jump_to_value;
        let segment_num = this.state.segment_num;
        return (!isNaN(parseFloat(jump_to_value)) && isFinite(jump_to_value)) &&
            0 <= jump_to_value && jump_to_value <= this.state.maximum_jump_allowed &&
            !(jump_to_value > segment_num && !this.allQuestionsAreCompleted());
    };

    handleJumpToButton = () => {
        if (this.userCanJump()) {
            this.gotoSegment(this.state.jump_to_value);
        }
    };

    toOverview () {
        this.sendData(false);
        this.setState({current_view: VIEWS.OVERVIEW})
    }

    toggleAddEvidenceMode(is_document_question, question_id) {
        const ems = this.state.evidenceModeState;
        if (ems.active) {
            if (ems.is_document_question !== is_document_question
                || ems.question_id !== question_id) {
                return;  // ignore clicks from other buttons
            } else if (this.state.current_selection.toString() !== "") {
                this.addEvidence(is_document_question, question_id);
            }
        }
        ems.active = !ems.active;
        ems.is_document_question = is_document_question;
        ems.question_id = question_id;
        this.setState({evidenceModeState: ems});
    }

    handleSelectionDragEnd() {
        this.setState({
            current_selection: window.getSelection(),
        });
    }

    addEvidence(is_document_question, question_id) {
        const new_evidence = this.state.current_selection.toString();

        // eslint-disable-next-line no-unused-vars
        const [response, _responseArr] =
            this.getOrCreateResponseObjectAndArray(is_document_question, question_id);

        let new_evidence_arr;
        if (response.evidence === undefined) {
            new_evidence_arr = [new_evidence];
        } else {
            new_evidence_arr = response.evidence.slice();
            new_evidence_arr.push(new_evidence);
        }

        const update_dict = {
            evidence: new_evidence_arr,
        }
        this.updateResponseObject(is_document_question, question_id, update_dict);
    }

    handleRemoveEvidence(is_document_question, question_id, evidence_index) {
        // eslint-disable-next-line no-unused-vars
        const [response, _responseArr] =
            this.getOrCreateResponseObjectAndArray(is_document_question, question_id);
        const evidence = response.evidence;
        const updated_evidence_arr =
            evidence.slice(0, evidence_index).concat(evidence.slice(evidence_index + 1));
        const update_dict = {
            evidence: updated_evidence_arr,
        }
        this.updateResponseObject(is_document_question, question_id, update_dict);
    }

    buildQuestionFields(questions, is_document_question) {
        return questions.map((question, id) => {
            // eslint-disable-next-line no-unused-vars
            const [response, responseArr] =
                this.getOrCreateResponseObjectAndArray(is_document_question, question.id);
            return (
                <Question
                    key={id}
                    question={question}
                    response={response}
                    is_document_question={is_document_question}
                    evidenceModeState={this.state.evidenceModeState}
                    handleResponseChange={
                        (e) => this.handleResponseChange(is_document_question, question.id, e)
                    }
                    toggleAddEvidenceMode={
                        () => this.toggleAddEvidenceMode(is_document_question, question.id)
                    }
                    handleRemoveEvidence={
                        (is_doc_q, q_id, evidence_idx) =>
                            this.handleRemoveEvidence(is_doc_q, q_id, evidence_idx)
                    }
                />
            );
        });
    }

    handleStudentName(e) {
        this.setState({student_name: e.target.value});
    }

    render() {
        if (this.state.current_view === VIEWS.INSTRUCTIONS_NAME) {
            return (
                <InstructionsNameView
                    handleStudentName={this.handleStudentName}
                    startReading={this.startReading}
                />

            )
        }

        const doc = this.state.document;
        if (!doc) {
            return ( <div>Loading!</div> );
        }

        const current_segment = doc.segments[this.state.segment_num];
        const segment_questions = current_segment.questions;
        const document_questions = doc.document_questions;
        const overview_questions = doc.overview_questions;

        // Generate response fields for each of the questions
        const segment_response_fields = this.buildQuestionFields(segment_questions, false);
        const document_response_fields = this.buildQuestionFields(document_questions, true);

        // Hardcoded roman numeral conversions for now.
        const roman_numeral = { 1: "I", 2:"II", 3:"III", 4:"IV", 5:"V", 6:"VI", 7:"VII"};

        return (
            <div className="container py-5">
                <div className="row mb-4"><div className="col">
                    <h1 className="display-4">
                        {doc.title} <span className="author">by {doc.author}</span>
                    </h1>
                </div></div>

                {this.state.current_view === VIEWS.OVERVIEW &&
                    <OverviewView
                        all_segments={doc.segments}
                        document_questions={document_questions}
                        overview_questions={overview_questions}
                        buildQuestionFields={this.buildQuestionFields}
                    />
                }
                {this.state.current_view === VIEWS.READING &&
                    <React.Fragment>
                        <div className="row">
                            <div className="col-12">
                                <h5 className="segment-num">
                                    Segment {roman_numeral[this.state.segment_num + 1]}
                                </h5>
                                <hr/>
                            </div>
                            <div className='segment-container'>
                                <Segment
                                    text={current_segment.text}
                                    handleScroll={(e) => this.handleScroll(e)}
                                    segment_ref={this.segment_ref}
                                    handleSelectionDragEnd={() => this.handleSelectionDragEnd()}
                                />
                            </div>

                            <div className="questions-container">
                                {this.state.rereading && segment_response_fields}
                                {this.state.rereading && document_response_fields}
                                <NavBar
                                    document_segments={doc.segments}
                                    segment_num={this.state.segment_num}
                                    rereading={this.state.rereading}
                                    prevSegment={this.prevSegment}
                                    nextSegment={this.nextSegment}
                                    toOverview={this.toOverview}
                                    handleJumpToFieldChange={this.handleJumpToFieldChange}
                                    handleJumpToButton={this.handleJumpToButton}
                                    handleJumpToFieldKeyDown={this.handleJumpToFieldKeyDown}
                                    userCanJump={this.userCanJump}
                                />
                            </div>
                        </div>
                    </React.Fragment>
                }
            </div>
        );
    }
}
