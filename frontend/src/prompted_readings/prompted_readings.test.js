import React from 'react';
import ReactDOM from 'react-dom';
import CommonResponses from './analysis_view';
import App from './student_view';
import {
    FrequencyFeelingTable,
    ContextVsViewTime,
    SentimentScores,
    MeanReadingTimesForQuestions,
} from "./analysis_view";

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

it('FrequencyFeelingTable renders without crashing', () => {
    const div = document.createElement('div');
    const test_data = [
        ["happy", 30],
        ["surprised", 15],
    ];
    ReactDOM.render(<FrequencyFeelingTable feelings={test_data} />, div);
    ReactDOM.unmountComponentAtNode(div);
});

it('ContextVsViewTime renders without crashing', () => {
    const div = document.createElement('div');
    const test_data = {
        "This is a story": 2.873,
        "This is an ad": 3.987,
    };
    ReactDOM.render(<ContextVsViewTime viewTime={test_data}/>, div);
    ReactDOM.unmountComponentAtNode(div);
});

it('renders SentimentScores without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<SentimentScores />, div);
    ReactDOM.unmountComponentAtNode(div);
});

it('MeanReadingTimesForQuestions renders without crashing', () => {
    const div = document.createElement('div');
    const test_data = [
        ['In one word, how does this text make you feel?', 'This is an ad.', 3.84, 30],
        ['In one word, how does this text make you feel?',
            'This is actually a short story.', 2.22, 30],
        ['In three words or fewer, what is this text about?', 'This is an ad.', 1.89, 8],
        ['In three words or fewer, what is this text about?',
            'This is actually a short story.', 0.97, 1],
        ['Have you encountered this text before?', 'This is an ad.', 1.78, 1],
        ['Have you encountered this text before?', 'This is actually a short story.', 0, 0]
    ];
    ReactDOM.render(<MeanReadingTimesForQuestions
        mean_reading_times_for_questions={test_data} />, div);
    ReactDOM.unmountComponentAtNode(div);
});
