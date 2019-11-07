import React from "react";
import PropTypes from 'prop-types';
import './reading_view.css';

class Segment extends React.Component {
    render() {
        return (
            <div>
                <p>Segment Number: {this.props.segmentNum + 1}</p>
                <div className="scroll_segment">
                    {this.props.segmentLines.map((line, k) => (
                        <p key={k}>{line}</p>)
                    )}
                </div>
            </div>
        )
    }
}
Segment.propTypes = {
    segmentLines: PropTypes.array,
    segmentNum: PropTypes.number,
};

class ReadingWindow extends React.Component {
    render() {
        return (
            <div>
                <div className={"row"}>
                    <div className={'col-8'}>
                        {/*<Segment*/}
                        {/*    segmentLines={segment_lines}*/}
                        {/*    segmentNum={this.state.segment_num}*/}
                        {/*/>*/}
                        <button
                            className={"btn btn-outline-dark mr-2"}
                            onClick={() => this.prevSegment()}
                        >
                            Back
                        </button>
                        <button
                            className={"btn btn-outline-dark"}
                            onClick={() => this.nextSegment()}
                        >
                            {this.state.rereading ? 'Next' : 'Reread'}
                        </button>
                    </div>
                </div>
            </div>
        )
    }
}

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
                    <p><b>Overview Questions</b></p>
                    {this.props.document_questions.map((el, i) => (
                        <p key={i}>{el}</p>)
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

class OverviewView extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            segment_num: 71,
            timer: null,
            segment_data: [],
            scrollTop: 0,
            scroll_ups: 0,
            scrolling_up: false,
            rereading: false,  // we alternate reading and rereading
            document: null,
            overview: false
        }
    }

    async componentDidMount() {
        try {
            // Hardcode the document we know exists for now,
            // Generalize later...
            const response = await fetch('/api/documents/1');
            const document = await response.json();
            this.setState({document});
            window.addEventListener('scroll', this.handleScroll, true);
        } catch (e) {
            console.log(e);
        }

    }


    render() {
        const doc = this.state.document;

        if (doc) {
            // const current_segment = doc.segments[this.state.segment_num];
            // const segment_text = current_segment.text;
            // const segment_lines = segment_text.split("\r\n");
            // const segment_questions = current_segment.questions;
            // const segment_contexts = current_segment.contexts;
            const all_segments = doc.segments;
            const document_questions = ["placeholder1", "placeholder2"];
            // document questions PR isn't on but it will be soon

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{doc.title}</h1>
                    {this.state.rereading ? <OverviewWindow
                        all_segments={all_segments}
                        document_questions={document_questions}
                    /> : <ReadingWindow />}

                </div>
            );
        } else {
            return (
                <div>Loading!</div>
            );
        }

    }
}

export default OverviewView;
