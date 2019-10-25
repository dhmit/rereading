import React from "react";
import {TimeIt, handleStoryScroll} from "../common";
// import PropTypes from 'prop-types';

// This is a document object hardcoded here for prototyping,
// to be replaced with an object fetched via API call once that's ready
const document = {
    title: "The Pigs",
    prompts: ["the author is alive", "the book was written during the cold war"],
    segments: [
        {
            text: "The little pig built a house",
            seq: 0,
            prompts: ["this is an ad"],
            questions: [
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
            ]
        },
        {
            text: "The wolf huffed and puffed",
            seq: 1,
            prompts: ["this is a story", "the author is testing you"],
            questions: [
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
            ]
        },
        {
            text: "The pigs have brick house so they are safe.",
            seq: 2,
            prompts: ["this is a poem"],
            questions: [
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
            ]
        },
    ]
};


class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 0,
            timer: null,
            segmentReadTimes: [],
            scrollTop: 0,
            scroll_ups: 0,
            scrolling_up: false,
        }
    }

    /**
     * segmentReadTimes is a array of arrays. The index of each array
     * corresponds to the segment number of the segments and is updated
     * with a new time every time the buttons are clicked
     */
    restartTimer(firstTime) {
        if (!firstTime) {
            const segmentReadTimes = this.state.segmentReadTimes;
            const time = this.state.timer.stop();
            segmentReadTimes[this.state.segmentNum].push(time);
            this.setState({segmentReadTimes,});
        }
        const timer = new TimeIt();
        this.setState({timer});
    }

    changeSegment (changeNum) {
        const segmentNum = this.state.segmentNum + changeNum;
        // document will be replaced by actual data
        if (segmentNum >= 0 && segmentNum < document.segments.length){
            this.restartTimer(false);
            this.setState({segmentNum,});
        }
    }

    componentDidMount() {
        this.restartTimer(true);
        let segmentReadTimes = this.state.segmentReadTimes;
        for (let i = 0; i < document.segments.length; i++){
            segmentReadTimes.push([]);
        }
        this.setState({segmentReadTimes,});
    }

    /**
     * Soon we will replace all instances of `document` with the actual data that
     * you fetch from the API
     */
    render() {
        const data = document;
        return (
            <div className={"container"} onScroll={(e) =>
            {this.setState(handleStoryScroll(e, this.state))}}>
                <h1>{data.title}</h1>
                <p><b>Prompts: </b>{data.prompts.map(el => "[" + el + "] ")}</p>
                <p>Segment Number: {this.state.segmentNum + 1}</p>
                <p style={{fontSize: "300px"}}>{data.segments[this.state.segmentNum].text}</p>
                {this.state.segmentNum > 0 ?
                    <button onClick = {() => this.changeSegment(-1)}>Back</button> :
                    ""}
                {this.state.segmentNum < document.segments.length - 1 ?
                    <button onClick={() => this.changeSegment(1)}>Next</button> :
                    ""}
            </div>
        );
    }
}

export default ReadingView;

