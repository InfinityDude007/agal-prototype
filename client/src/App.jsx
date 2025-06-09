import { useState, useEffect } from 'react'
import ReactMarkdown from 'react-markdown';
import './App.css'
import api from './utils/api.js';



function App() {


	const [rootRes, setRootRes] = useState('');
	const [healthRes, setHealthRes] = useState({});

	const [modelRes, setModelRes] = useState('');
	const [modelResTime, setModelResTime] = useState('');

	const testData = {
		project_type: "build a new factory",
		project_goal: "increase revenue, production capacity, outreach and market share",
		company_industry: "electric vehicles, mainly cars",
		investment: "€5,000,000,000",
		countries: "France, Germany, or USA"
	}

	const [userData, setUserData] = useState({
		project_type: "",
		project_goal: "",
		company_industry: "",
		investment: "",
		countries: "",
	});
	const [formError, setFormError] = useState("");

	const handleUserFormSubmit = () => {
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
		fetchModelRes(userData);
		setIsUserSel(true);
		setInputFor('User Input');
	};

	const [inputFor, setInputFor] = useState('Test Data');
	const [isUserSel, setIsUserSel] = useState(false);
	useEffect(() => {
		if (modelRes) {
			setIsUserSel(false);
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

			<h2 className='analysis-h2'>Feasibility Analysis</h2>
			{(!modelRes && !isUserSel) && (
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
									fetchModelRes(testData);
									setIsUserSel(true);
									setInputFor('Test Data');
								}}
							>Submit</button>							
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
							<button className='submit' onClick={() => handleUserFormSubmit()}>Submit</button>
				
						</div>
					</div>
				</div>
			)}

			{isUserSel && (
				<>
					<p className='loading-p'><strong>Generating Report</strong></p>
					<TimeElapsed active={isUserSel && !modelRes} />
					<p className='loading-p'><strong>Data:</strong> {inputFor}</p>
					<div class="loader" />
				</>
			)}
			{modelRes && (
				<>						
					<button className='clearRes' onClick={() => setModelRes('')}>Clear</button>
					<br />
					<span><strong>Response Time:</strong> {modelResTime}</span>
				</>
			)}
			{modelRes && (
				<div className="resBlock-model">			
					<span className="value">
						<ReactMarkdown>
							{modelRes}
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
