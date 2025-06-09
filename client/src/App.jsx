import { useState } from 'react'
import './App.css'
import api from './utils/api.js';



function App() {


	const [rootRes, setRootRes] = useState('')
	const [healthRes, setHealthRes] = useState([])


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


			<div className='buttonGroup'>
				<button className='getRes' onClick={fetchRoot}>Fetch Root</button>
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
