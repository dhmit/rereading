import React from "react";
import {TimeIt, handleStoryScroll} from "../common";
import './reading_view.css';
import PropTypes from 'prop-types';

class Segment extends React.Component {
    render() {
        return (
            <div className="scroll">
                <p>Segment Number: {this.props.segment_num + 1}</p>
                {this.props.segmentLines.map((line, k) => (
                    <p key={k}>{line}</p>)
                )}
            </div>
        )
    }
}
Segment.propTypes = {
    segmentLines: PropTypes.array,
    segment_num: PropTypes.number,
};


class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 0,
            timer: null,
            segment_data: [],
            segments_viewed: [0],
            scrollTop: 0,
            scroll_ups: 0,
            scrolling_up: false,
            rereading: false,  // we alternate reading and rereading
            document: null,
        }
    }

    /**
     * segment_read_times is a array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with a new time every time the buttons are clicked
     */
    updateData(firstTime){
        if (!firstTime) {
            const segment_data = this.state.segment_data;
            const time = this.state.timer.stop();
            segment_data.push({
                scroll_ups: this.state.scroll_ups,
                read_time: time,
                is_rereading: this.state.rereading,
                segment_num: this.state.segment_num
            });
            this.setState({segment_data, scroll_ups: -1});
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    // We have the big arrow notation here to bind "this" to this function
    handleScroll = (e) => {
        this.setState(handleStoryScroll(e, this.state.scrollTop, this.state.scroll_ups,
            this.state.scrolling_up));
    };

    prevSegment () {
        this.gotoSegment(this.state.segment_num - 1);
        this.updateData(false);
        window.scrollTo(0,0);
    }

    nextSegment () {
        this.updateData(false);
        if (this.state.rereading) {
            // If we're already rereading, move to the next segment
            this.gotoSegment(this.state.segment_num + 1);
        } else {
            // Otherwise, move on to the rereading layout
            this.setState({rereading: true});
        }
        window.scrollTo(0,0);
    }

    gotoSegment(segmentNum) {
        const segments_viewed = this.state.segments_viewed.slice();
        let rereading = segments_viewed.includes(segmentNum);

        //The segment number is pushed regardless of whether or not the user has read the page
        // before so that page reread order can also be determined.
        segments_viewed.push(segmentNum);
        console.log(segments_viewed);
        this.setState({rereading, segments_viewed, segment_num : segmentNum});
    }

    async componentDidMount() {
        try {
            // Hard code the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            this.setState({document});
            this.updateData(true);
            // This will allow the scroll detector to work
            /** TODO: Add event listener to the reading pane when it is complete to track scroll
             *        data on that reading pane only. Currently, it is tracking scrolling data
             *        for entire page
             */
            window.addEventListener('scroll', this.handleScroll, true);
        } catch (e) {
            console.log(e);
        }

    }

    render() {
        const doc = this.state.document;

        if (doc) {
            const current_segment = doc.segments[this.state.segment_num];
            const segment_text = current_segment.text;
            const segment_lines = segment_text.split("\r\n");
            const segment_questions = current_segment.questions;
            const segment_contexts = current_segment.contexts;
            const document_questions = doc.document_questions;

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{doc.title}</h1>
                    <div className={"row"}>
                        <Segment
                            segmentLines={segment_lines}
                            segment_num={this.state.segment_num}
                        />
                        <div className={'col-8'}>
                            <button
                                className={"btn btn-outline-dark mr-2"}
                                onClick={() => this.prevSegment()}
                                disabled={this.state.segment_num === 0}
                            >
                                Back
                            </button>
                            <button
                                className={"btn btn-outline-dark"}
                                onClick={() => this.nextSegment()}
                                disabled={this.state.rereading &&
                                this.state.segment_num >= doc.segments.length - 1}
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
