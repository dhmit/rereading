import React from "react";
import {TimeIt, handleStoryScroll} from "../common";
// import PropTypes from 'prop-types';

// THIS IS JUST FOR PROTOTYPING
// DELETE ME as soon as these data are included in the API endpoint
const PROMPTS_PROTOTYPE = ["this is an ad"];
const QUESTIONS_PROTOTYPE = [
    {
        question: "question_test",
        is_free_response: true,
        choices: [],
    },
    {
        question: "question_test2",
        is_free_response: false,
        choices: ["yes", "no"],
    },
];

class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 0,
            timer: null,
            segment_data: [],
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
        this.updateData(false);
        this.setState({segment_num: this.state.segment_num-1});
        window.scrollTo(0,0);
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
        window.scrollTo(0,0);
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
            /** TODO: For when reading pane is done
             *  Add event listener to the reading pane when it is complete to track scroll data
             *  on that reading pane only. Currently, it is tracking scrolling data for entire page
             */
            window.addEventListener('scroll', this.handleScroll, true);
        } catch (e) {
            console.log(e);
        }

    }

    render() {
        const data = this.state.document;

        if (data) {
            const questions = QUESTIONS_PROTOTYPE; // replace me with this.state.document.whatever
            const prompts = PROMPTS_PROTOTYPE; // replace me with this.state.document.whatever
            const segment = data.segments[this.state.segment_num].text;

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{data.title}</h1>
                    <div className={"row"}>
                        <div className={"col-9"}>
                            <p>Segment Number: {this.state.segment_num + 1}</p>
                            <p>{segment}</p>
                            {this.state.segment_num > 0 &&
                            <button
                                className={"btn btn-outline-dark mr-2"}
                                onClick={() => this.prevSegment()}
                            >
                                Back
                            </button>
                            }
                            <button
                                className={"btn btn-outline-dark"}
                                onClick={() => this.nextSegment()}
                            >
                                {this.state.rereading ? 'Next' : 'Reread'}
                            </button>
                        </div>

                        {this.state.rereading &&
                            <div className={"analysis col-3"}>
                                <p><b>Prompts: </b>{prompts.map(el => "[" + el + "] ")}</p>
                                <p><b>Questions: </b>
                                    {questions.map(el => "[" + el.question + "] ")}
                                </p>
                                <p><b>Add an annotation: </b><input
                                    type="text"
                                    value={this.state.value}
                                    onChange={this.handleChange}
                                /><button>Submit</button></p>
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
