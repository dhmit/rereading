import React from 'react';
import ReactDOM from 'react-dom';
import App from './student_view';
import SentimentScores from './analysis_view';

it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<App />, div);
    ReactDOM.unmountComponentAtNode(div);
});

it('renders SentimentScores without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<SentimentScores />, div);
    ReactDOM.unmountComponentAtNode(div);
});
