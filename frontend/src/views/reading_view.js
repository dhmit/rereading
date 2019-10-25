import React from "react";
// import PropTypes from 'prop-types';

// This is a document object hardcoded here for prototyping,
// to be replaced with an object fetched via API call once that's ready
const document = {
    title: "The Pigs",
    prompts: ["the author is alive", "the book was written during the cold war"],
    segments: [
        {
            text: "The little pig built a house.",
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
        }
    }

    changeSegment (changeNum) {
        const newNum = this.state.segmentNum + changeNum;
        // document will be replaced by actual data
        if (newNum >= 0 && newNum < document.segments.length){
            this.setState({segmentNum: newNum});
        }
    }

    render() {
        const data = document;
        return (
            <div className={"container"}>
                <h1>{data.title}</h1>
                <p><b>Prompts: </b>{data.prompts.map(el => "[" + el + "] ")}</p>
                <p>Segment Number: {this.state.segmentNum + 1}</p>
                <p>{data.segments[this.state.segmentNum].text}</p>
                <button onClick = {() => this.changeSegment(-1)}>Back</button>
                <button onClick = {() => this.changeSegment(1)}>Next</button>
            </div>
        );
    }
}

export default ReadingView;
