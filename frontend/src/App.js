import { useState } from "react";

const App = () => {
	const [dates, setDates] = useState({
		start: null,
		end: null,
	});

	const updateStartDate = (event) => {
		let currentDates = dates;
		currentDates.start = event.target.value;
		setDates(currentDates);
	};

	const updateEndDate = (event) => {
		let currentDates = dates;
		currentDates.end = event.target.value;
		setDates(currentDates);
	};

	const updateData = (data) => {
		const conHigh = document.getElementById("conversion-rate-high");
		const conLow = document.getElementById("conversion-rate-low");
		const conAvg = document.getElementById("conversion-rate-avg");
		const corraHigh = document.getElementById("corra-rate-high");
		const corraLow = document.getElementById("corra-rate-low");
		const corraAvg = document.getElementById("corra-rate-avg");
		const pearsonCoeff = document.getElementById("pearson-coeff");
		const error_msg = "Not enough data found to calculate.";

		// Set element content to data if its not null, otherwise set to the error msg
		conHigh.textContent = data["usd/cad"]["high"] || error_msg;
		conLow.textContent = data["usd/cad"]["low"] || error_msg;
		conAvg.textContent = data["usd/cad"]["average"] || error_msg;
		corraHigh.textContent = data["corra"]["high"] || error_msg;
		corraLow.textContent = data["corra"]["low"] || error_msg;
		corraAvg.textContent = data["corra"]["average"] || error_msg;
		pearsonCoeff.textContent = data["pearson_coeff"] || error_msg;
	};

	const makeRequest = () => {
		// Do nothing if no dates have been selected
		if (dates.start === null || dates.end === null) {
			return;
		}

		// Fetch data from API and update gui to reflect information
		fetch("/api", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				start: dates.start,
				end: dates.end,
			}),
		})
			.then((response) => response.json())
			.then((data) => updateData(data));
	};

	return (
		<div>
			<label>Start Date: </label>
			<input type="date" onChange={updateStartDate} />
			<br />

			<label>End Date: </label>
			<input type="date" onChange={updateEndDate} />
			<br />

			<button onClick={makeRequest}>Submit</button>

			<p>
				USD/CAD High: <span id="conversion-rate-high"></span>
			</p>
			<p>
				USD/CAD Low: <span id="conversion-rate-low"></span>
			</p>
			<p>
				USD/CAD Average: <span id="conversion-rate-avg"></span>
			</p>
			<p>
				CORRA High: <span id="corra-rate-high"></span>
			</p>
			<p>
				CORRA Low: <span id="corra-rate-low"></span>
			</p>
			<p>
				CORRA Average: <span id="corra-rate-avg"></span>
			</p>
			<p>
				Pearson Coefficient of Correlation: <span id="pearson-coeff"></span>
			</p>
		</div>
	);
};

export default App;
