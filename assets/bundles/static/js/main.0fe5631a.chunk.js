(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{43:function(t,e,n){t.exports=n(81)},50:function(t,e,n){},76:function(t,e,n){},81:function(t,e,n){"use strict";n.r(e);var a=n(0),s=n.n(a),r=n(18),o=n.n(r),i=n(40),c=n(12),l=(n(48),n(15)),u=n.n(l),h=n(19),m=n(20),d=n(21),p=n(23),v=n(22),f=n(24),y=(n(50),n(17)),b=n.n(y),w=n(38),x=n.n(w),E=n(39),k=n.n(E);function g(t){return s.a.createElement("div",{className:"question"},s.a.createElement("div",{className:"question-prompt"},t.question),s.a.createElement("form",{onSubmit:t.onSubmit},s.a.createElement("label",null,s.a.createElement(x.a.Control,{type:"text",value:t.answer,onChange:t.onChange})),s.a.createElement("div",null,s.a.createElement(b.a,{variant:"primary",type:"submit",size:"lg",block:!0},"Continue"))),s.a.createElement(b.a,{variant:"secondary",onClick:t.goBack,size:"lg",block:!0},"Go back to story"))}function _(t){return s.a.createElement("div",{className:"story"},s.a.createElement("div",{className:"context-text"},t.context),s.a.createElement("div",{className:"story-text"},t.story),s.a.createElement(b.a,{variant:"secondary",onClick:t.onClick,size:"lg",block:!0},"Continue"))}function S(t){return t.word_alert?s.a.createElement("div",{className:"word-alert"},s.a.createElement(k.a,{variant:"danger"},"Please make sure to enter a response and respect word limits")):null}var C=function(t){function e(t){var n;return Object(m.a)(this,e),(n=Object(p.a)(this,Object(v.a)(e).call(this,t))).state={story:null,contexts:[],questions:[],context_number:0,question_number:0,answers:[],finished:!1,start:!0,textInput:"",views:0,show_story:!0,word_alert:!1},n}return Object(f.a)(e,t),Object(d.a)(e,[{key:"componentDidMount",value:function(){var t=Object(h.a)(u.a.mark(function t(){var e,n;return u.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,fetch("http://localhost:8000/api/");case 3:return e=t.sent,t.next=6,e.json();case 6:n=t.sent,this.setState(n[0]),t.next=13;break;case 10:t.prev=10,t.t0=t.catch(0),console.log(t.t0);case 13:case"end":return t.stop()}},t,this,[[0,10]])}));return function(){return t.apply(this,arguments)}}()},{key:"postData",value:function(){var t={story:this.state.story,student_responses:this.state.answers};console.log(JSON.stringify(t)),fetch("http://localhost:8000/api/add-response/",{method:"POST",body:JSON.stringify(t),headers:{"Content-type":"application/json"}}).then(function(t){return t.json()}).then(function(t){return console.log(JSON.stringify(t))}).catch(function(t){return console.log(t)})}},{key:"handleFormChange",value:function(t){this.setState({textInput:t.target.value})}},{key:"validateSubmission",value:function(t,e){return!!t&&t.trim().split(" ").length<=e}},{key:"handleSubmit",value:function(t){t.preventDefault();var e=this.state.question_number,n=this.state.context_number,a=this.state.answers.slice(),s=this.state.textInput,r=this.state.views,o=this.state.questions[e].word_limit,i=this.state.finished,c=this.state.show_story;if(this.validateSubmission(s,o)){var l={context:this.state.contexts[n],question:this.state.questions[e].text,response:s,views:r};a.push(l),r=0,e<this.state.questions.length-1?e+=1:n<this.state.contexts.length-1?(n+=1,e=0,c=!0):i=!0,this.setState({question_number:e,context_number:n,answers:a,finished:i,textInput:"",show_story:c,views:r,word_alert:!1})}else this.setState({word_alert:!0})}},{key:"handleStartClick",value:function(){this.setState({start:!1})}},{key:"toggleStory",value:function(){var t=!this.state.show_story,e=this.state.views;t&&e++,this.setState({show_story:t,views:e})}},{key:"render",value:function(){var t,e=this;return this.state.story?this.state.start?t=s.a.createElement("div",{className:"start"},s.a.createElement("div",null,"Are you ready?"),s.a.createElement(b.a,{variant:"secondary",onClick:function(){return e.handleStartClick()},size:"lg",block:!0},"Start!")):this.state.finished?(this.postData(),t=s.a.createElement("div",{className:"finished"},"Thank you for your time!")):t=this.state.show_story?s.a.createElement(_,{story:this.state.story,context:this.state.contexts[this.state.context_number],onClick:function(){return e.toggleStory()}}):s.a.createElement("div",null,s.a.createElement("div",null,s.a.createElement(S,{word_alert:this.state.word_alert})),s.a.createElement("div",null,s.a.createElement(g,{story:this.state.story,context:this.state.contexts[this.state.context_number],question:this.state.questions[this.state.question_number].text,onChange:function(t){return e.handleFormChange(t)},onSubmit:function(t){return e.handleSubmit(t)},answer:this.state.textInput,goBack:function(){return e.toggleStory()}}))):t=null,t}}]),e}(s.a.Component);n(76);var j=function(t){function e(t){var n;return Object(m.a)(this,e),(n=Object(p.a)(this,Object(v.a)(e).call(this,t))).state={data:[]},n}return Object(f.a)(e,t),Object(d.a)(e,[{key:"componentDidMount",value:function(){var t=Object(h.a)(u.a.mark(function t(){var e,n;return u.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,fetch("http://127.0.0.1:8000/api/add-response");case 3:return e=t.sent,t.next=6,e.json();case 6:n=t.sent,this.setState({data:n}),t.next=13;break;case 10:t.prev=10,t.t0=t.catch(0),console.log(t.t0);case 13:case"end":return t.stop()}},t,this,[[0,10]])}));return function(){return t.apply(this,arguments)}}()},{key:"render",value:function(){return s.a.createElement("div",null,this.state.data.map(function(t){return s.a.createElement("div",{key:t.id},s.a.createElement("h1",null,"Story: ",t.story),s.a.createElement("h3",null,"Context: ",t.student_responses[0].context),s.a.createElement("p",null,"Questions: ",t.student_responses[0].question),s.a.createElement("p",null,"Response: ",t.student_responses[0].response),s.a.createElement("p",null,"Views: ",t.student_responses[0].views))}),";")}}]),e}(s.a.Component),O=s.a.createElement(i.a,null,s.a.createElement("div",null,s.a.createElement(c.a,{path:"/student",component:C}),s.a.createElement(c.a,{path:"/instructor",component:j})));o.a.render(O,document.getElementById("root"))}},[[43,1,2]]]);
//# sourceMappingURL=main.0fe5631a.chunk.js.map