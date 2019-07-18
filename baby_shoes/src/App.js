import React from 'react';
import './App.css';

const list = [
    {
        id: 0,
        story: 'Baby shoes. Never worn.',
        contexts: ['This is an ad.', 'This is a story.'],
        questions: [
            {
                text: 'In one word or less, how did this make you feel?',
                word_limit: 1,
            },
            {
                text: 'In three words or less, what is this story about?',
                word_limit: 3,
            },
        ],
    },
];

function Question(props) {
    return (
        <div className={'story'}>
            <div className={'story-text'}>{props.story}</div>
            <div className={'question-prompt'}>{props.question}</div>
            <form>
                <label>
                    <input type={'text'} value={props.answer} onChange={props.onChange} />
                </label>
            </form>
        </div>
    );
}

class Study extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            story: null,
            contexts: [],
            questions: [],
            context_number: 0,
            question_number: 0,
            is_start: true,
            answers: [[]],
        };

    }

    componentDidMount() {
        // Load from server
        this.setState(list[0])
    }

    handleFormChange(e, context, question) {
        const responses = this.state.answers.slice();

        if (responses[context][question]) {
            responses[context][question] = e.target.value;
        } else {
            responses[context] = [e.target.value];
        }

        this.setState({answers: responses})
    }



    render() {

        let response;
        if (this.state.story) {
            response = (<Question
                story={this.state.story}
                question={this.state.questions[this.state.question_number]['text']}
                onChange={(e) => this.handleFormChange(e, this.state.context_number, this.state.question_number)}
                answer={this.state.answers[this.state.context_number][this.state.question_number]}
            />);
        } else {
            response = null;
        }

        return response;
    }
}

export default Study;
