//slide de imagini

var i = 0;
var images = [];

images[0] = 'Gardener.png';
images[1] = 'Doctor.png';
images[2] = 'Thief.png';
images[3] = 'Lawyer.png';

function changeImg(){
	document.slide.src=images[i];
	
	if(i < images.length -1) { i++; }
	else { i=0; }
	
	setTimeout("changeImg()", 2000);
	
}

window.onload = changeImg;


//quiz

const startButton = document.getElementById('start-btn');
const nextButton = document.getElementById('next-btn');
const questionContainerElement = document.getElementById('question-container');
let shuffledQuestions, currentQuestionIndex;

const questionElement= document.getElementById('question');
const answerButtonsElement= document.getElementById('answer-buttons');

startButton.addEventListener('click', startQuiz);
nextButton.addEventListener('click', () =>{
	currentQuestionIndex++;
	setNextQuestion();
});

function startQuiz(){
	
	startButton.classList.add('hide');
	shuffledQuestions = questions.sort( () => Math.random() -.5);
	currentQuestionIndex = 0;
	questionContainerElement.classList.remove('hide');
	setNextQuestion();
}

function setNextQuestion(){
	resetState();
	showQuestion(shuffledQuestions[currentQuestionIndex]);
}

function showQuestion(question){
	questionElement.innerText = question.question;
	question.answers.forEach( answer =>{
		const button = document.createElement('button');
		button.innerText = answer.text;
		button.classList.add('btn');
		if(answer.correct){
			button.dataset.correct = answer.correct;
		}
		button.addEventListener('click', selectAnswer);	
		answerButtonsElement.appendChild(button);
	})
}

function resetState(){
	nextButton.classList.add('hide');
	while (answerButtonsElement.firstChild){
		answerButtonsElement.removeChild(answerButtonsElement.firstChild);
	}
}

function selectAnswer(e){
	const selectedButton = e.target;
	const correct = selectedButton.dataset.correct;
	Array.from(answerButtonsElement.children).forEach(button => {
		setStatusClass(button, button.dataset.correct)
	})
	if(shuffledQuestions.length > currentQuestionIndex  + 1){
		nextButton.classList.remove('hide');
	}
	else
	{
		startButton.innerText = 'Restart Quiz';
		startButton.classList.remove('hide');
	}
}

function setStatusClass(element, correct){
	clearStatusElement(element);
	if(correct){
		element.classList.add('correct');
	}
	else{
		element.classList.add('wrong');
	}
}

function clearStatusElement(element){
	element.classList.remove('correct');
	element.classList.remove('wrong');
}

const questions = [
{
	question: 'Who is gardener s father?',
	answers:
		[	
		{ text:'Leo Beck', correct: true},
		{ text:'Freddy Riley', correct: false},
		{ text:'Kreacher Pierson', correct: false},
		{ text:'Jack', correct: false}
		]
},

{
	question: 'What funded Mr. Kreacher Pierson ?',
	answers:
		[	
		{ text:'A museum', correct: false},
		{ text:'A church', correct: false},
		{ text:'An orphanage', correct: true},
		{ text:'A school', correct: false}
		]
},

{
	question: 'Who killed Emma s mother?',
	answers:
		[	
		{ text:'Leo Beck', correct: false},
		{ text:'Freddy Riley', correct: false},
		{ text:'Kreacher Pierson', correct: false},
		{ text:'Emily Dyer', correct: true}
		]
},

{
	question: 'Who is Kreacher Pierson obssesed with?',
	answers:
		[	
		{ text:'Emma Woods', correct: true},
		{ text:'Leo Beck', correct: false},
		{ text:'Freddy Riley', correct: false},
		{ text:'Emily Dyer', correct: false}
		]
},

{
	question: 'What job did Emily Dyer have?',
	answers:
		[	
		{ text:'She was a teacher.', correct: false},
		{ text:'She was a painter.', correct: false},
		{ text:'She was a doctor.', correct: true},
		{ text:'She was a gardener.', correct: false}
		]
}
]


//numar de cate ori a fost facut quiz-ul
function clickCounter() {
  if(typeof(Storage) !== "undefined") {
    if (localStorage.clickcount) {
      localStorage.clickcount = Number(localStorage.clickcount)+1;
    } else {
      localStorage.clickcount = 1;
    }
    document.getElementById("result").innerHTML = "The quiz was completed a number of " + localStorage.clickcount + " time(s).";
  } else {
    document.getElementById("result").innerHTML = "Sorry, your browser does not support web storage...";
  }
}