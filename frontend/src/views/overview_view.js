import React from "react";
//import PropTypes from 'prop-types';

export class OverviewView extends React.Component {
    render() {
        return (
            <div>
                <nav className={"navbar navbar-expand-lg"}>
                    <div className={"navbar-nav"}>
                        <a
                            className={"nav-link nav-item text-dark font-weight-bold"}
                            href={"#"}
                        >Project</a>
                        <a
                            className={"nav-link nav-item text-dark font-weight-bold"}
                            href={"#"}
                        >The Reading Sample</a>
                        <a
                            className={"nav-link nav-item text-dark font-weight-bold"}
                            href={"#"}
                        >Rereading Visuals</a>
                        <a
                            className={"nav-link nav-item text-dark font-weight-bold"}
                            href={"#"}
                        >Rereading Values</a>
                    </div>
                </nav>
                <h1>The Reading Redux</h1>
                <h3>The Values of Rereading</h3>
                <p>
                    In literary studies we have a word to describe a novel that traces the
                    psychological and moral growth of its protagonist. The word is
                    <em> bildungsroman.</em> But I think it is at once strange and unfortunate that
                    we have no such word to describe a category of research or writing that traces
                    the development of a real-life reader of a novel. This glaring lacuna might be a
                    consequence of the fact that we just do not have that kind of data. That is, we
                    do not know enough about if, how, or how much a reader evolves via each
                    encounter with a text. In a time when it seems that bigots are getting bolder
                    and louder all while basically insisting that they are surfeited with learning
                    new things, which could actually help make them more tolerant (and tolerable)
                    people, it is perhaps consoling to remember that human beings are in fact
                    changeable. Reading is essential to
                    galvanizing those human changes. This Digital Humanities project wants to
                    affirm this claim by studying the effects of the practice of
                    <em> re-reading</em> a work
                    of literature. The scope of the project includes, but is not limited to, an
                    attempt to answer the following questions: If we can understand the outcomes of
                    re-reading a text, then what might we be able to deduce about how formative a
                    text really is and how people think differently, change their minds, or become
                    entirely different people as time goes by?
                </p>
                <ul>
                    <li>
                        What can we discover about how exactly a reader is reading
                        <em> differently</em> when we evaluate what that reader annotates
                        differently
                        upon rereading a text?
                    </li>
                    <li>
                        How many re-readings and over the course of how long a period of time does
                        it take to generate different meanings of one text? Is there a way to direct
                        or expedite that process of readers making new meanings?
                    </li>
                    <li>
                        What are the various factors that motivate people to reread texts in the
                        first place?
                    </li>
                    <li>
                        What kinds of literary texts are especially conducive to answering this
                        project’s questions?
                    </li>
                    <li>
                        When a reader’s understanding of the meaning of a text changes over time,
                        how can we attribute this change to how the reader has also changed over
                        time—whether with respect to age, mentality, political perspective, gender,
                        etc.?
                    </li>
                </ul>
                <p>
                    At least one positive consequence of this project I anticipate is that the
                    nagging question in literacy-education circles about how to help people
                    transform into better readers can become less about trying to get people to read
                    <em> more</em> and perhaps more about trying to get people to read, again and
                    again (and at different stages in their lives), some of the texts already in
                    their stock of
                    texts to read. Indeed, while reproducibility is a scientific aspiration required
                    to conduct scientific experiments, the kind of repetition with a difference that
                    I hope to study here underscores not only how different the Humanities is from
                    the Sciences but also how the Humanities <em> needs</em> to be different from
                    scientific
                    protocols in order to make clear that humanists value a changing human in an
                    inevitably changing world. I envision this project being useful to students
                    interested in learning how to appreciate the value of rereading books; to
                    instructors who want and need to make the texts that they re-teach, year in and
                    year out, “come alive” not only for their students but also for themselves; to
                    cognitive psychologists curious about the re-reading mind; to a general audience
                    of readers eager to understand both the qualitative and quantitative uses of
                    literature.
                </p>
            </div>
        );
    }
}
