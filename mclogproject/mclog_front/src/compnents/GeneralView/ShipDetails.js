import React from 'react'
import './ShipDetails.css'
import axios from 'axios'
import {LineChart,  Line, CartesianGrid, XAxis, YAxis, BarChart, Tooltip, Legend, Bar } from 'recharts';


const baseURL="http://127.0.0.1:8000";

function DownTime(){
    return(
        <p>test</p>
    )
};

class GeneralView extends React.Component{
    constructor(props){
        super(props);
        this.state={
            shipResponse:[],
            shipScenario:"",
            shipNames:[],
            logCategory:["Warning","Info","Fault","Deactivated"],
            data : [
                {
                  "name": "Page A",
                  "uv": 4000,
                  "pv": 2400
                },
                {
                  "name": "Page B",
                  "uv": 3000,
                  "pv": 1398
                },
                {
                  "name": "Page C",
                  "uv": 2000,
                  "pv": 9800
                },
                {
                  "name": "Page D",
                  "uv": 2780,
                  "pv": 3908
                },
                {
                  "name": "Page E",
                  "uv": 1890,
                  "pv": 4800
                },
                {
                  "name": "Page F",
                  "uv": 2390,
                  "pv": 3800
                },
                {
                  "name": "Page G",
                  "uv": 3490,
                  "pv": 4300
                }],
        };
        
        
        this.handleChange=this.handleChange.bind(this);
    };
    
    componentDidMount(){
        axios.get(`${baseURL}`)
        .then((response)=> {
                this.setState({shipNames: response.data
                });
            });
    };
    
    // downtime(){
    //     axios.get(`${baseURL}/downtime`)
    //     .then((response)=>{
    //         this.setState({shipResponse:response.data})
    //     })
    // };

    // extendOpenPosition(){
    //     axios.get(`${baseURL}/extendopen`)
    //     .then((response)=>{
    //         this.setState({shipResponse:response.data})
    //     })
    // };

    handleChange(event){
        this.setState({shipScenario:event.target.value});
        // console.log(this.state.shipScenario);
        axios.get(`${baseURL}/${event.target.value}`)
        .then((response)=>{
            this.setState({shipResponse:response.data})
        })

        console.log(this.state.shipResponse);
    };

    render(){
        return(
            <div className="container">
                <div className="row align-items-center p-2">
                    <div className="col">
                         <div className='p-2 g-1 border bg-light'>
                            <label>
                                Ship IMO
                            </label>
                            <select name='IMO'>
                                <option>From database</option>
                            </select>
                        </div>

                        <div className='p-2 g-1 border bg-light'>
                            <label>
                                Ship Name
                            </label>
                            <select name='Ship name'>
                                {
                                    this.state.shipNames.map((name)=>(
                                        <option key={name}>{name}</option>
                                    ))
                                }
                            </select>
                        </div>

                        {/* <div className='p-2 g-1 border bg-light'>
                            <button>Get Ship</button>
                        </div> */}
                    
                    <div className='p-2 g-1 border bg-light'>
                        <label>
                            Date From
                        </label>
                        <input type="date"></input>
                        <label>To:</label>
                        <input type="date"></input>
                    </div>

                    <div className='p-2 g-1 border bg-light'>
                        <label>
                            Log category
                        </label>
                        <select name="logCategory">
                            {
                                this.state.logCategory.map((category)=>(
                                    <option key={category}>{category}</option>
                                ))
                            }
                        </select>
                    </div>

                    <div className='p-2 g-1 border bg-light'>
                        <label>
                            Scenario query
                        </label>
                        <select name='Scenario' onChange={this.handleChange}>
                            <option value="downtime">System downtime</option>
                            <option value="extendopen">Extend open position</option>
                        </select>
                    </div>

                    <div className='p-2 g-1 border bg-light'>
                        {this.state.shipResponse.map((res)=>(
                            <li key={this.state.shipResponse.indexOf(res)} >{res.toString()}</li>
                        ))
                        }
                     </div>
                 
                        
                    <div className='p-2 g-1 border bg-light'>
                    <BarChart width={800} height={250} data={this.state.data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="pv" fill="#8884d8" />
                        <Bar dataKey="uv" fill="#82ca9d" />
                    </BarChart>
                    </div>

                    

               </div>     
               
            </div>
        </div>
        )
    }
}

export default GeneralView;