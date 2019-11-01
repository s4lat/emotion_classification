const EMOTIONS_RUS = ["Злость" ,"Отвращение","Испуг", "Счастье", "Грусть", "Удивление",
 "Спокойствие"]

var total = 0;
var score = 0;
var images = null;
var quizImage = null;
var goodAnsw = null;
var answers= [];

function init_quiz(){
	window.total = 0;
	window.score = 0;
	window.answers = []
	let img_ind = Math.floor(Math.random() * images.length);
	window.quizImage = images[img_ind];
	window.images.splice(img_ind, 1);
	window.goodAnsw = parseInt(quizImage.split(".")[0].split("%")[1]);
}

function check_answer(answ){
	window.total += 1;
	if (answ == window.goodAnsw){
		window.score += 1;
	}

	answers.push(["../static/quiz/" + window.quizImage, window.goodAnsw, answ]);

	if (images.length == 0){
		$.ajax({
        type : 'GET',
        url : 'get_image_list',
        success : function(data){
			window.images = data;
			let img_ind = Math.floor(Math.random() * window.images.length);
			window.quizImage = window.images[img_ind];
			window.images.splice(img_ind, 1);
			window.goodAnsw = parseInt(window.quizImage.split(".")[0].split("%")[1]);
			update_quiz();
        }});

	} else {
		let img_ind = Math.floor(Math.random() * images.length);
    	window.quizImage = window.images[img_ind];
    	window.images.splice(img_ind, 1);
    	window.goodAnsw = parseInt(window.quizImage.split(".")[0].split("%")[1]);
    	update_quiz();
	}
}

function update_quiz(){
	$("#quizImg").attr("src", "../static/quiz/" + window.quizImage);
	$("#totalLabel").text(`Пройдено: ${total}`);
}

function finish_quiz(){
	$("#total_result").text(`Пройдено: ${window.total}`);
	$("#total_good").text(`Верно: ${window.score}`);
	$("#total_bad").text(`Неверно: ${window.total-window.score}`);

	window.draw_result();

	$("#quiz_row").hide();
	$("#result_row").show();
	$("#start_btn_row").show();
}

function draw_result(){
	let answersByEmotions = []
	for (let i=0; i<7; i++){
		answersByEmotions[i] = [0, 0];
	}

	for (let answ of window.answers){
		answersByEmotions[answ[1]][0] += 1;
		answersByEmotions[answ[1]][1] += answ[1] == answ[2] ? 1:0;
	}


	let trace1 = {
		x: ['Злость', 'Отвращение', 'Испуг', 'Счастье', 'Грусть', 'Удивление', 'Спокойствие'],
		y: [answersByEmotions[0][1],
			answersByEmotions[1][1],
			answersByEmotions[2][1],
			answersByEmotions[3][1],
			answersByEmotions[4][1],
			answersByEmotions[5][1],
			answersByEmotions[6][1]],
		name: 'Верные ответы',
		marker: { color: '#00cd00'},
		type: 'bar'
	};

	let trace2 = {
		x: ['Злость', 'Отвращение', 'Испуг', 'Счастье', 'Грусть', 'Удивление', 'Спокойствие'],
		y: [answersByEmotions[0][0] - answersByEmotions[0][1],
			answersByEmotions[1][0] - answersByEmotions[1][1],
			answersByEmotions[2][0] - answersByEmotions[2][1],
			answersByEmotions[3][0] - answersByEmotions[3][1],
			answersByEmotions[4][0] - answersByEmotions[4][1],
			answersByEmotions[5][0] - answersByEmotions[5][1],
			answersByEmotions[6][0] - answersByEmotions[6][1]],
		marker: { color: '#BC0F0F'},
		name: 'Неверные ответы',
		type: 'bar'
	};

	let data = [trace1, trace2];

	let layout = {
		barmode: 'stack',
	};

	Plotly.newPlot('result_plots', data, layout, {responsive: true});

	let answers_list = document.getElementById("answers_list")

	let previous_answs = answers_list.children

	while(previous_answs[2]) {
		previous_answs[2].parentNode.removeChild(previous_answs[1]);
	};

	let answ_template = document.getElementById("answ_row_template");

	// window.total += window.total % 3;

	let rows_n = Math.floor(window.total / 2);
	let cols_n = 2

	window.total % cols_n ? rows_n++:null;
	// console.log("ROWS_N ", rows_n)

	for (let i=0; i < rows_n; i++){
		let row = answ_template.cloneNode(true);

		if (i+1 == rows_n) 
			cols_n = (window.total % 2) ? window.total % 2:cols_n;

		for (let j=0; j < cols_n; j++){
			let answ = answers[(i*2)+j];
			let col = row.children[j];

			col.getElementsByTagName("img")[0].src = answ[0];

			let p = col.getElementsByTagName("p")
			p[0].innerHTML = `Вопрос #${i*2+j+1}`;
			p[1].innerHTML = `Верный ответ: ${EMOTIONS_RUS[answ[1]]}`;
			p[2].innerHTML = `Ответ тестируемого: ${EMOTIONS_RUS[answ[2]]}`;

			if (answ[1] == answ[2]){
				col.classList.add("border", "border-success");
			} else
			{
				col.classList.add("border", "border-danger");
			}

		}

		if (cols_n < 2){
			for (let k=0; k < 2 - cols_n; k++){
				row.children[cols_n+k].innerHTML = '';
			}
		}

		row.classList.remove("d-none");
		answers_list.append(row);
	}

}