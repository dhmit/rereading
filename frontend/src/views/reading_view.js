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
            <React.Fragment>
                <div className="row">
                    <div className="col">
                        {!on_last_segment_and_rereading
                            ? (
                                <button
                                    className="next-btn"
                                    onClick={() => this.props.nextSegment()}
                                >
                                    {this.props.rereading ? 'Next' : 'Continue'}
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
            </React.Fragment>
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
};


/*
 * A component to show the user their responses in the overview view
 */
class OverviewQuestionDisplay extends React.Component {
    render() {
        const q_and_r = this.props.question_and_response;
        const q = q_and_r.question;
        const r = q_and_r.response;
        return (
            <div className="card mb-5">
                <div className="card-header">
                    <div className='segment-question-text question-text'>
                        {q.text}
                    </div>
                </div>
                <div className="card-body">
                    {r.response}
                </div>
            </div>
        );
    }
}
OverviewQuestionDisplay.propTypes = {
    question_and_response: PropTypes.object,
}


class OverviewView extends React.Component {
    render() {
        const full_document_text = [];
        this.props.all_segments.map((el) => full_document_text.push(el.text.split("\r\n")));
        console.log(this.props.reading_data);
        const segment_data = this.props.reading_data.segment_data;
        const rereadings = segment_data.filter((datum) => datum.is_rereading);

        let all_responses = [];
        for (const rereading of rereadings) {
            all_responses = all_responses.concat(rereading.segment_responses);
        }

        let all_questions = [];
        for (const segment of this.props.all_segments) {
            const segment_questions = segment.questions;
            all_questions = all_questions.concat(segment_questions);
        }

        const question_and_responses = [];
        for (const response of all_responses) {
            const q = all_questions.find((q) => q.id === response.question);
            question_and_responses.push({
                question: q,
                response,
            });
        }

        return (
            <div className="row overview-container">
                <div className="col-12"><hr/></div>
                <div className="segment-container">
                    <div className="scroll-overview">
                        {full_document_text.map((segment_text_array) => (
                            segment_text_array.map((text, i) => (
                                <p className={"segment-text text-justify"} key={i}>{text}</p>
                            ))
                        ))}
                    </div>
                </div>
                <div className="questions-container">
                    <p>
                        Thank you for participating! Here is a summary of your responses:
                    </p>
                    {question_and_responses.map((q_and_r, i) =>
                        <OverviewQuestionDisplay key={i} question_and_response={q_and_r} />
                    )}
                    <button
                        className="next-btn"
                        onClick={() => window.location.href = '../project_overview'}
                    >Finish Reading
                    </button>
                </div>
            </div>
        );
    }
}
OverviewView.propTypes = {
    all_segments: PropTypes.array,
    reading_data: PropTypes.object,
};

export class InstructionsNameView extends React.Component {
    render() {
        return (
            <div className={"container"}>
                <h1 className={"display-4 text-center mt-4 title"}>
                    Instructions
                </h1>
                <div className={"mb-5 instructions"}>
                    <p id={"instructions-overview"}>
                        Do a close reading of the text by following these steps:
                        Read all five segments of the text one segment at a time, while answering
                        questions for each segment along the way (including the two common
                        questions that recur for each segment).
                    </p>
                    <ol id={"instructions-list"}>
                        <li>
                            After you read through the whole segment, click the “Continue” button
                            in order to access the questions for that particular segment.
                        </li>
                        <li>
                            As often as you need to, scroll through the segment in order to provide
                            an answer for each question posed for that segment.
                        </li>
                        <li>
                            Provide evidence for questions that require evidence by clicking
                            “Add Evidence,” highlighting the words or passages from the segment
                            you want to add, then clicking “Stop Tagging”.
                            Repeat this process as many times as there are other pieces of evidence
                            from the segment you want to add.
                        </li>
                        <li>
                            After you’ve answered all questions and added evidence for a segment,
                            click the “Next” button in order to access the next segment.
                        </li>
                    </ol>
                    <h4 className="title">Enter your name or leave blank to remain anonymous</h4>
                    <div className={"input-group"}>
                        <input
                            className={"form-control"}
                            type={"text"}
                            onChange={(e) => this.props.handleStudentName(e)}
                        />
                        <div className={"input-group-append"}>
                            <button
                                className={"btn start-btn "}
                                onClick={() => this.props.startReading()}
                            >
                                Start Reading
                            </button>
                        </div>
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
            segments_viewed: [0],
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
        };
        this.scroll_data = [];
        this.csrftoken = getCookie('csrftoken');

        this.segment_ref = React.createRef();
        this.allQuestionsAreCompleted = this.allQuestionsAreCompleted.bind(this);
        this.nextSegment = this.nextSegment.bind(this);
        this.toOverview = this.toOverview.bind(this);
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
            const interval_timer = setInterval(() => this.recordScroll(), 1000);
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

    async sendData(firstTime){
        if (!firstTime) {
            const time = this.state.timer.stop();
            const url = '/api/add-response/';
            const reading_data = {
                reading_data_id: this.state.reading_data.id,
                segment_data: [{
                    id: this.state.document.segments[this.state.segment_num].id,
                    scroll_data: JSON.stringify(this.scroll_data),
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
            this.scroll_data = [];
            this.setState({reading_data: new_reading_data});
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    recordScroll() {
        this.scroll_data.push(this.state.scroll_top);
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

        if (document_responses.length === document_questions.length
            && segment_responses.length === segment_questions.length) {
            for (const el of document_responses) {
                if (el.response.trim() === "") {
                    return false;
                }
                const dq = document_questions.find((dq) => dq.id === el.id);
                if (dq.require_evidence) {
                    if (el.evidence === undefined || el.evidence.length === 0) {
                        return false;
                    }
                }
            }
            for (const el of segment_responses) {
                if (el.response.trim() === ""){
                    return false;
                }
                const sq = segment_questions.find((sq) => sq.id === el.id);
                if (sq.require_evidence) {
                    if (el.evidence === undefined || el.evidence.length === 0) {
                        return false;
                    }
                }
            }
        } else {
            return false;
        }

        return true;
    }

    checkScrolledToBottom() {
        const segment_dom_el = this.segment_ref.current;

        const scroll_remaining = segment_dom_el.scrollHeight - segment_dom_el.scrollTop;

        // leave a little room for floating point error and general fuzziness
        const is_at_bottom = Math.abs(scroll_remaining - segment_dom_el.offsetHeight) < 5;

        if (is_at_bottom) {
            return true;
        }

        return false;
    }

    nextSegment () {
        if (this.state.rereading) {
            // If we're already rereading, move to the next segment
            this.gotoSegment(this.state.segment_num + 1);
        } else {
            // Otherwise, move on to the rereading layout, if user has scrolled to the bottom
            if (!this.checkScrolledToBottom()) {
                alert('Please read and scroll to the bottom of the segment before moving on.');
                return;
            }
            this.sendData(false);
            this.segment_ref.current.scrollTo(0,0);
            this.setState({rereading: true});
        }
    }

    validateData() {
        // Check if all questions are completed if advancing
        if (!this.allQuestionsAreCompleted()) {
            alert("Please respond to every question and add evidence where indicated " +
                "before moving on.");
            return false
        }
        return true;
    }

    gotoSegment(target_segment_num) {
        if (!this.validateData()) { return; }

        this.sendData(false);
        this.segment_ref.current.scrollTo(0,0);
        const segments_viewed = this.state.segments_viewed.slice();

        // Store the current segment reading data into state
        const segmentResponseArray = [];

        const rereading = segments_viewed.includes(target_segment_num);
        segments_viewed.push(target_segment_num);

        this.setState({
            rereading,
            segments_viewed,
            segment_num: target_segment_num,
            segmentQuestionNum: 0,
            segmentResponseArray,
        });
    }

    toOverview () {
        if(!this.validateData()) { return; }

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

        // Generate response fields for each of the questions
        const segment_response_fields = this.buildQuestionFields(segment_questions, false);
        const document_response_fields = this.buildQuestionFields(document_questions, true);

        // Hardcoded for now...
        const roman_numeral_and_segment_date = {
            1: "I - circa 1950s",
            2: "II - circa 1960s",
            3: "III - circa 1970s",
            4: "IV - circa 1970s",
            5: "V - circa 1980s",
        };

        return (
            <div className="container background py-3">
                <div className="row mb-4"><div className="col">
                    <h1 className="display-4 title">
                        {doc.title} <span className="author">by {doc.author}</span>
                    </h1>
                </div></div>

                {this.state.current_view === VIEWS.OVERVIEW &&
                    <OverviewView
                        all_segments={doc.segments}
                        reading_data={this.state.reading_data}
                    />
                }
                {this.state.current_view === VIEWS.READING &&
                    <React.Fragment>
                        <div className="row text-and-questions">
                            <div className="col-12">
                                <h5 className="segment-num">
                                    Segment {
                                        roman_numeral_and_segment_date[this.state.segment_num + 1]
                                    }
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
                                />
                            </div>
                        </div>
                    </React.Fragment>
                }
            </div>
        );
    }
}
