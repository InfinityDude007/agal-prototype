import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './App.css';
import api from './utils/api.js';



function App() {


	const [rootRes, setRootRes] = useState('');
	const [healthRes, setHealthRes] = useState({});

	const [financialRes, setFinancialRes] = useState({});
	const [reportPage, setReportPage] = useState(1);
	const totalPages = 2;

	const [modelRes, setModelRes] = useState('');
	const [modelResTime, setModelResTime] = useState('');

	const testData = {
		project_type: "build a new factory",
		project_goal: "increase revenue, production capacity, outreach and market share",
		company_industry: "electric vehicles, mainly cars",
		investment: "€5,000,000,000",
		countries: "France, Germany, or USA"
	}

	const testFinancials = {
		"investment": 5000000000,
		"cash_flows": [758650000, 1560521677, 2764034047, 2483023988, 2713071166, 2730335737, 3029161512, 2857978747, 2863915475, 2913778177],
		"discount_rates": [0.08, 0.10],
		"capex_adjustments": [-0.15, 0.15]
	}

	const [userData, setUserData] = useState({
		project_type: "",
		project_goal: "",
		company_industry: "",
		investment: "",
		countries: "",
	});

	const [tempUserFinancials, setTempUserFinancials] = useState({
		investment: "",
		cash_flows: [],
		cash_flows_string: "",
		discount_rate_1: "",
		discount_rate_2: "",
		capex_adjustment: ""
	})

	const [userFinancials, setUserFinancials] = useState({
		investment: 0,
		cash_flows: [],
		discount_rates: [],
		capex_adjustments: []
	})

	const [formError, setFormError] = useState("");

	const handleUserDataFormSubmit = () => {
		if (
			!userData.project_type.trim() ||
			!userData.project_goal.trim() ||
			!userData.company_industry.trim() ||
			!userData.investment.trim() ||
			!userData.countries.trim()
		) {
			setFormError("Please fill in all the fields");
			return;
		}
		setFormError("");
		setInputFor('User Input');
		setIsUserFin(true)
	};

	const handleUserFinFormSubmit = () => {
		const cash_flows = tempUserFinancials.cash_flows;
		const discount_rate_1 = Number(tempUserFinancials.discount_rate_1);
		const discount_rate_2 = Number(tempUserFinancials.discount_rate_2);
		const capex_adjustment = Number(tempUserFinancials.capex_adjustment);
		const investmentStr = userData.investment || "";
		const investment = Number(investmentStr.replace(/[^0-9.-]/g, ""));

		if (
			!investment ||
			!Array.isArray(cash_flows) || cash_flows.length === 0 || cash_flows.some(cf => isNaN(cf) || cf <= 0) ||
			!discount_rate_1 || isNaN(Number(discount_rate_1)) ||
			!discount_rate_2 || isNaN(Number(discount_rate_2)) ||
			!capex_adjustment || isNaN(Number(capex_adjustment))
		) {
			setFormError("Please fill in all the fields");
			return;
		}
		const finalFin = {
			investment: tempUserFinancials.investment,
			cash_flows: tempUserFinancials.cash_flows,
			discount_rates: [
				tempUserFinancials.discount_rate_1 * 0.01,
				tempUserFinancials.discount_rate_2 * 0.01
			],
			capex_adjustments: [
				tempUserFinancials.capex_adjustment * -0.01,
				tempUserFinancials.capex_adjustment * 0.01
			]
		};
		setUserFinancials(finalFin);
		setFormError("");
		setInputFor("Input Data");
		setIsUserFin(false);
		setIsUserSel(true);
		fetchFinancialRes(finalFin, userData);
	};

	const [inputFor, setInputFor] = useState('Test Data');
	const [isUserSel, setIsUserSel] = useState(false);
	const [isUserFin, setIsUserFin] = useState(false);
	useEffect(() => {
		if (modelRes) {
			setIsUserSel(false);
			setIsUserFin(false);
		}
	}, [modelRes]);


	const fetchRoot = async () => {
		try {
			const response = await api.get('/');
			setRootRes(response.data.message);
		
		} catch (error) {
			console.error("Error fetching root:", error)
		}
	};


	const fetchHealth = async () => {
		try {
			const response = await api.get('/health');
			setHealthRes(response.data);
		
		} catch (error) {
			console.error("Error fetching root:", error)
		}
	};


	useEffect(() => {
		fetchRoot();
		fetchHealth();
	}, []);


	const fetchFinancialRes = async (finData, modelData) => {
		try {
			const response = await api.post('calculate-financials',
				{
					investment: finData.investment,
					cash_flows: finData.cash_flows,
					discount_rates: finData.discount_rates,
					capex_adjustments: finData.capex_adjustments
				}
			);
			setFinancialRes(response.data);
		} catch (error) {
			console.error("Error calculating financial values:", error)
		}
		setTimeout(() => {
			fetchModelRes(modelData);
		}, 1000);
	};


	const fetchModelRes = async (data) => {
		try {
			const response = await api.post('/query-model', 
				{
					project_type: data.project_type,
					project_goal: data.project_goal,
					company_industry: data.company_industry,
					investment: data.investment,
					countries: data.countries
				}
			);
			setModelRes(response.data.model_response);
			setModelResTime(response.data.inference_time);

		} catch (error) {
			console.error("Error fetching model response:", error)
		}
	};


	function TimeElapsed({ active }) {
		const [seconds, setSeconds] = useState(0);

		useEffect(() => {
			if (!active) {
				setSeconds(0);
				return;
			}
			setSeconds(0);

			const interval = setInterval(() => {
				setSeconds((prev) => prev + 1);
			}, 1000);
			return () => clearInterval(interval);
			
		}, [active]);

		if (!active) return null;
		return (
			<p className='loading-p'>
				<strong>Time Elapsed:</strong> {seconds} second{seconds !== 1 ? "s" : ""}
			</p>
		);
	}


	return (
		<div className='main'>

			<h1>
				<img src='mvp-icon.svg' />
				AGAL Prototype - Test Interface
			</h1>

			{(!modelRes && !isUserSel && !isUserFin) && (
				<div className='analysis'>
					<div className='analysis-group-1'>
						<div className='resBlock-form'>
							<p className='analysis-p'><strong>Test Data</strong></p>
							<div className='testData'>
								<span className='testDataLabel'>Project Type</span>
								<span className='testDataValue'>Build a new factory</span>
								<span className='testDataLabel'>Project Goal</span>
								<span className='testDataValue'>Increase revenue, production capacity, outreach and market share</span>
								<span className='testDataLabel'>Company Industry</span>
								<span className='testDataValue'>Electric vehicles, mainly cars</span>
								<span className='testDataLabel'>Investment Amount</span>
								<span className='testDataValue'>€5,000,000,000</span>
								<span className='testDataLabel'>Prospective Countries</span>
								<span className='testDataValue'>France, Germany, or USA</span>
							</div>				
							<button
								className='submit'
								onClick={() => {
									setInputFor('Test Data');
									setIsUserFin(true);
								}}
							>Next</button>
						</div>
					</div>
			
					<div className='analysis-group-2'>
						<div className='resBlock-form'>
							<p className='analysis-p'><strong>Input Data</strong></p>

							<form
								className='form'
								autoComplete="off"
							>
								<label className='formLabel' htmlFor='form_projectType'>Project Type</label>
								<input
									type="text"
									id='form_projectType'
									className='formInput'
									placeholder="(e.g. Department expansion, new factory)"
									value={userData.project_type}
									onChange={e => setUserData({ ...userData, project_type: e.target.value })}
									required
								/>
								<label className='formLabel' htmlFor='form_projectGoal'>Project Goal</label>
								<input
									type="text"
									id='form_projectGoal'
									className='formInput'
									placeholder="(e.g. Revenue growth, outreach)"
									value={userData.project_goal}
									onChange={e => setUserData({ ...userData, project_goal: e.target.value })}
									required
								/>
								<label className='formLabel' htmlFor='form_companyIndustry'>Company Industry</label>
								<input
									type="text"
									id='form_companyIndustry'
									className='formInput'
									placeholder="(e.g. Technology, mainly phones)"
									value={userData.company_industry}
									onChange={e => setUserData({ ...userData, company_industry: e.target.value })}
									required
								/>
								<label className='formLabel' htmlFor='form_investmentAmount'>Investment Amount</label>
								<input
									type="text"
									id='form_investmentAmount'
									className='formInput'
									placeholder="(e.g. €5,000,000,000)"
									value={userData.investment}
									onChange={e => setUserData({ ...userData, investment: e.target.value })}
									required
								/>
								<label className='formLabel' htmlFor='form_countries'>Prospective Countries</label>
								<input
									type="text"
									id='form_countries'
									className='formInput'
									placeholder="(e.g. India, Germany, USA)"
									value={userData.countries}
									onChange={e => setUserData({ ...userData, countries: e.target.value })}
									required
								/>
								{!formError && <div className='form-error-hidden'></div>}	
								{formError && <div className='form-error'>{formError}</div>}								
							</form>
							<button className='submit' onClick={() => handleUserDataFormSubmit()}>Next</button>
				
						</div>
					</div>
				</div>
			)}


			{(!modelRes && isUserFin && (
				inputFor === "Test Data" ? (
					<div className='finData'>
						<div className='finData-group'>
							<div className='finData-form'>
								<p className='finData-p'><strong>Test Financial Data</strong></p>
								<div className='testData'>
									<span className='testDataLabel'>Investment</span>
									<span className='testDataValue'>5000000000</span>
									<span className='testDataLabel'>Cash Flows (Years 1 to 10, comma separated)</span>
									<span className='testDataValue-padded'>758650000, 1560521677, 2764034047, 2483023988, 2713071166, 2730335737, 3029161512, 2857978747, 2863915475, 2913778177</span>
									<span className='testDataLabel'>Discount Rate 1 (%)</span>
									<span className='testDataValue'>8</span>
									<span className='testDataLabel'>Discount Rate 2 (%)</span>
									<span className='testDataValue'>10</span>
									<span className='testDataLabel'>Capex Adjustment (±%)</span>
									<span className='testDataValue'>15</span>
								</div>
								<div className='finButton-group'>
									<button className='cancel' onClick={() => setIsUserFin(false)}>Cancel</button>			
									<button
										className='submit'
										onClick={() => {
											setInputFor('Test Data');
											setIsUserFin(false);
											setIsUserSel(true);
											fetchFinancialRes(testFinancials, testData);
										}}
									>Submit</button>
								</div>
							</div>
						</div>
					</div>
				) : (
					<div className='finData'>
						<div className='finData-group'>
							<div className='finData-form'>
								<p className='finData-p'><strong>Input Financial Data</strong></p>

								<form
									className='form'
									autoComplete="off"
								>
									<span className='testDataLabel'>Investment</span>
									<span className='testDataValue'>{userData.investment.replace(/[^0-9.-]/g, '') || "0"}</span>
									<label className='formLabel' htmlFor='form_cashFlows'>Cash Flows (Years 1 to 10, comma separated)</label>
									<textarea
										type="text"
										id='form_cashFlows'
										className='formInput-padded'
										placeholder="(e.g. 750000000, 1500000000, 2000000000, 2400000000, 2710000000, 2738000000, 3000000000, 2850000000...)"
										value={tempUserFinancials.cash_flows_string || ""}
										onChange={e => {
											const input = e.target.value;
											const parsed = input.split(',').map(s => Number(s.trim())).filter(n => !isNaN(n));
											setTempUserFinancials({ ...tempUserFinancials, cash_flows_string: input, cash_flows: parsed });
										}}
										required
									/>
									<label className='formLabel' htmlFor='form_discountRate1'>Discount Rate 1 (%)</label>
									<input
										type="text"
										id='form_discountRate1'
										className='formInput'
										placeholder="(e.g. 10)"
										value={tempUserFinancials.discount_rate_1}
										onChange={e => setTempUserFinancials({ ...tempUserFinancials, discount_rate_1: e.target.value })}
										required
									/>
									<label className='formLabel' htmlFor='form_discountRate2'>Discount Rate 2 (%)</label>
									<input
										type="text"
										id='form_discountRate2'
										className='formInput'
										placeholder="(e.g. 10)"
										value={tempUserFinancials.discount_rate_2}
										onChange={e => setTempUserFinancials({ ...tempUserFinancials, discount_rate_2: e.target.value })}
										required
									/>
									<label className='formLabel' htmlFor='form_capexAdjustments'>Capex Adjustment (±%)</label>
									<input
										type="text"
										id='form_capexAdjustments'
										className='formInput'
										placeholder="(e.g. 15)"
										value={tempUserFinancials.capex_adjustment}
										onChange={e => setTempUserFinancials({ ...tempUserFinancials, capex_adjustment: e.target.value })}
										required
									/>
									{!formError && <div className='form-error-hidden'></div>}	
									{formError && <div className='form-error'>{formError}</div>}								
								</form>

								<div className='finButton-group'>
									<button className='cancel' onClick={() => {setIsUserFin(false); setFormError("")}}>Cancel</button>			
									<button className='submit' onClick={() => handleUserFinFormSubmit()}>Submit</button>
								</div>
							</div>
						</div>
					</div>
				)
			))}


			{isUserSel && (
				<>
					<p className='loading-p'><strong>Generating Report</strong></p>
					<TimeElapsed active={isUserSel && !modelRes} />
					<p className='loading-p'><strong>Data:</strong> {inputFor}</p>
					<div className="loader" />
				</>
			)}
			{modelRes && (
				<>						
					<button className='clearRes' onClick={() => setModelRes('')}>Clear</button>
					<br />
					<div className='pageScroll'>
						<button
							className='pageButton'
							onClick={() => reportPage - 1 === 0 ? setReportPage(totalPages) : setReportPage(reportPage - 1)}
						>
							<svg
								className='pageButton-arrowLeft'
								viewBox="0 0 46 40"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"></path>
							</svg>
						</button>
						{reportPage === 1 && (
							<div className='pageHeader'>
								<h2><span>Feasibility Report</span></h2>
								<span><strong>Response Time:</strong> {modelResTime}</span>
							</div>
						)}
						{reportPage === 2 && (
							<div className='pageHeader'>
								<h2><span>Financial Report</span></h2>
							</div>
						)}
						<button
							className='pageButton'
							onClick={() => reportPage + 1 > totalPages ? setReportPage(1) : setReportPage(reportPage + 1)}
						>
							<svg
								className='pageButton-arrowRight'
								viewBox="0 0 46 40"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z"></path>
							</svg>
						</button>
					</div>
				</>
			)}
			{(modelRes && (reportPage === 1)) && (
				<div className="resBlock-model">			
					<span className="value">
						<ReactMarkdown
							remarkPlugins={[remarkGfm]}
							components={{
								table: ({node, ...props}) => <table className="markdown-table" {...props} />,
							}}
						>
							{modelRes}
						</ReactMarkdown>
					</span>
				</div>
			)}
			{(modelRes && (reportPage === 2)) && (
				<div className="resBlock-model">			
					<span className="value">
						<ReactMarkdown
							remarkPlugins={[remarkGfm]}
							components={{
								table: ({node, ...props}) => <table className="markdown-table" {...props} />,
							}}
						>
							{JSON.stringify(financialRes)}
						</ReactMarkdown>
					</span>
				</div>
			)}

			<h2 className='serverUtils-h2'>Server Utils</h2>
			<div className='serverUtils'>

				<div className='serverUtils-group-1'>
					<div className='buttonGroup'>
						<button className='getRes' onClick={() => fetchRoot()}>Fetch Root</button>
						{rootRes && (
							<button className='clearRes' onClick={() => setRootRes('')}>Clear</button>
						)}
					</div>
					{rootRes && (
						<div className="resBlock resBlock-grid">
							<span className="label"><strong>Message:</strong></span>
							<span className="value">{rootRes}</span> 
						</div>				
					)}
				</div>

				<div className='serverUtils-group-2'>
					<div className='buttonGroup'>
						<button className='getRes' onClick={() => fetchHealth()}>Fetch Health</button>
						{healthRes.message && (
							<button className='clearRes' onClick={() => setHealthRes({})}>Clear</button>
						)}
					</div>
					{healthRes.message && (
						<div className="resBlock resBlock-grid">
							<span className="label"><strong>Message:</strong></span>
							<span className="value">{healthRes.message}</span>
							<span className="label"><strong>Status:</strong></span>
							<span className="value">{healthRes.status}</span>
							<span className="label"><strong>Timestamp:</strong></span>
							<span className="value">{healthRes.timestamp}</span>
						</div>
					)}
				</div>

			</div>

		</div>
	);
}

export default App;
