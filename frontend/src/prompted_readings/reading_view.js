const document = {
    title: "test_title",
    prompts: ["the author is alive", "the book was written during the cold war"],
    segments: [
        {
            text: "",
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
            text: "test",
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
            text: "test2",
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
console.log(document);
