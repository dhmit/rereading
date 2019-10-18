import React from 'react';
import ReactDOM from 'react-dom';
import CommonResponses from './analysis_view';

it('renders without crashing', () => {
    const div = document.createElement('div');
    const test = [
        {
            "question": "In one word, how does this text make you feel?",
            "context": "This is an ad.",
            "answers": [
                "sad",
                "confused"
            ]
        },
        {
            "question": "In one word, how does this text make you feel?",
            "context": "This is actually a short story.",
            "answers": [
                "sad"
            ]
        },
    ]
    ReactDOM.render(<CommonResponses responses={test} />, div);
    ReactDOM.unmountComponentAtNode(div);
});

