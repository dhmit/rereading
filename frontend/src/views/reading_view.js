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

// const annotations = []


class ReadingView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segmentNum: 0,
            showing: false,
        }
    }

    changeSegment (changeNum) {
        const newNum = this.state.segmentNum + changeNum;
        // document will be replaced by actual data
        if (newNum >= 0 && newNum < document.segments.length){
            this.setState({segmentNum: newNum});
        }
        if (this.state.showing === true) {
            this.setState({showing: !this.state.showing});
        }
    }

    // addAnnotation (startIndex, endIndex) {
    //
    // }

    render() {
        const data = document;
        const questions = data.segments[this.state.segmentNum].questions;
        const segment = data.segments[this.state.segmentNum].text;

        return (
            <div className={"container"}>
                <h1>{data.title}</h1>
                <p>Segment Number: {this.state.segmentNum + 1}</p>
                <p>{segment}</p>
                <button onClick = {() => this.changeSegment(-1)}>Back</button>
                <button onClick = {() => this.changeSegment(1)}>Next</button>
                <button onClick = {() => this.setState({ showing: !this.state.showing })}>
                    Toggle analysis view</button>


                { this.state.showing &&
                    <div className={"analysis"}>
                        <p><b>Prompts: </b>{data.prompts.map(el => "[" + el + "] ")}</p>
                        <p><b>Questions: </b>{questions.map(el => "[" + el.question + "] ")}</p>
                        <p>{segment}</p>
                        <p><b>Add an annotation: </b><input
                            type="text"
                            value={this.state.value}
                            onChange={this.handleChange}
                        /><button>Submit</button></p>
                    </div>
                }
            </div>
            /* idea: maybe show the text again and allow highlighting and annotation (which
               would show on mouse hover using popover
             */
        );
    }
}

export default ReadingView;
