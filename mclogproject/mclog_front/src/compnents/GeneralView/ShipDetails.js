import React from 'react'
import './ShipDetails.css'
import axios from 'axios'


const baseURL="http://127.0.0.1:8000"

class GeneralView extends React.Component{
    constructor(props){
        super(props);
        this.state={
            shipResponse:[],
            shipScenario:"",
            shipNames:[],
        };
        
        this.handleChange=this.handleChange.bind(this);
    };
    
    componentDidMount(){
        axios.get(`${baseURL}`)
        .then((response)=> {
                this.setState({shipNames: response.data
                });
            })
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
        axios.get(`${baseURL}/${this.state.shipScenario}`)
        .then((response)=>{
            this.setState({shipResponse:response.data})
        })
    };

    render(){
        return(
            <div className="container">
            <div className="row align-items-start">
                <div className="col">
                    
                        <div>
                            <label>
                                Ship IMO
                            </label>
                            <select name='IMO'>
                                <option>From db</option>
                            </select>
                        </div>

                        <div>
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

                        <div>
                            <button>Get Ship</button>
                        </div>
                    
                    <div>
                        <label>
                            Date From:
                        </label>
                        <input type="date"></input>
                        <label>To:</label>
                        <input type="date"></input>
                    </div>

                    <div>
                        <label>
                            Log category
                        </label>
                        <select name='Log category'>
                            <option>From db</option>
                        </select>
                    </div>

                    <div>
                    <label>
                        Scenario query
                    </label>
                    <select name='Scenario' value={this.state.shipScenario} onChange={this.handleChange}>
                        
                        <option value="downtime">System downtime</option>
                        <option value="extendopen">Extend open position</option>
                    </select>
                    </div>

                </div>                    
            </div>
            <div className="row align-items-end">
                <div className="col">
                    <p>
                        Placeholder for the chart
                    </p>

                    
                    
                 </div>
            </div>
            
            <div>
                {this.state.shipResponse.map((res)=>(
                        <p key={this.state.shipResponse.indexOf(res)} >{res.toString()}</p>
                    ))
                    }
            </div>
        </div>
        )
    }
}

export default GeneralView;