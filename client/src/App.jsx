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

	return (
		<div className='main'>

			<h1>
				<img src='/public/mvp-icon.svg' />
				AGAL Test Interface
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

			<div className='buttonGroup'>
				<button className='getRes' onClick={fetchHealth}>Fetch Health</button>
				{healthRes.message && (
					<button className='clearRes' onClick={() => setHealthRes([])}>Clear</button>
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
	);
}

export default App;
