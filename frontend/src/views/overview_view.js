import React from "react";
import PropTypes from 'prop-types';

class OverviewWindow extends React.Component {
    render() {
        return (
            <div className={"row"}>
                <div className={"col-8"}>
                    {this.props.all_segments.map((el, i) => (
                        <p key={i}>{el.text}</p>)
                    )}
                </div>
                <div className={"col-4"}>
                    {this.props.document_questions.map((el, i) => (
                        <p key={i}>{el.text}</p>)
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
            segmentNum: 71,
            // MAKE SURE TO CHANGE THIS BACK TO 0
            // MAKE SURE TO CHANGE THIS BACK TO 0
            // MAKE SURE TO CHANGE THIS BACK TO 0
            // MAKE SURE TO CHANGE THIS BACK TO 0
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
        } catch (e) {
            console.log(e);
        }

    }


    render() {
        const data = this.state.document;

        if (data) {
            const all_segments = data.segments;
            const document_questions = data.questions; //document questions PR isn't on it but
            // it will be soon

            return (
                <div className={"container"}>
                    <h1 className={"display-4 py-3 pr-3"}>{data.title}</h1>
                    <OverviewWindow
                        all_segments={all_segments}
                        document_questions={document_questions}
                    />

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
