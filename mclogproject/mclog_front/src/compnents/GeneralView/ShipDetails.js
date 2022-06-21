import React from 'react'
import './ShipDetails.css'
import axios from 'axios'


const baseURL="http://127.0.0.1:8000";

class GeneralView extends React.Component{
    constructor(props){
        super(props);
        this.state={
            shipResponse:[],// server response
            getShipImos:[], // server response
            shipScenario:"", // scenairo string to for the req
            setShipImo:[], // single imo for the req
            shipNames:[], // server response
            logCategory:["Warning","Info","Fault","Deactivated"],
            scenarioDescription:
            [
            "How often the system is powered off and how long it stays without power.",
            "How often they continue operating to ext open position.",
            "Cases where position calibration is started but never done correctly.",
            ]
        };    
          this.handleChange=this.handleChange.bind(this);
    };
    
    // to get imo from db
    componentDidMount(){
        axios.get(`${baseURL}`)
        .then(response=> this.setState({getShipImos:response.data}))
        .catch(error=>console.log(error))
    };
    
    // to pass req to backend and get res from db
    // here need to get single imo + single scenario + date then create req
    handleChange(event){
        this.setState({shipScenario:event.target.value});
        axios.get(`${baseURL}/${event.target.value}`)
        .then((response)=>{
            this.setState({shipResponse:response.data})
        })
    };

    render()
    {      
        return(
            <div className="container">
                <div className="row align-items-center p-2">
                    <div className="col">
                        
                        <div className='p-2 g-1 border bg-success bg-gradient'>
                            <h2>Log file statistics</h2>
                        </div>
                        
                         <div className='p-2 g-1 border bg-light'>
                            <label>
                                Ship IMO
                            </label>
                            <select name='IMO'>
                                {   this.state.getShipImos.map((imo)=>(
                                    <option key={imo} >{imo}</option>
                                ))
                                    }
                            </select>
                        </div>

                        <div className='p-2 g-1 border bg-info shadow p-3 mb-1 bg-body rounded'>
                            <label>
                                Scenario query
                            </label>
                            <select name='Scenario' id="listOfScenairo" onChange={this.handleChange}>
                                <option value="downtime">System downtime</option>
                                <option value="extendopen">Extend open position</option>
                                <option value="calibration">Calibration difference</option>
                                <option value="stall">Stall fault</option>
                            </select>
                        </div>
                    
                        <div className='p-2 g-1 border bg-light'>
                            <label>
                                Date From
                            </label>
                            <input type="date"></input>
                            <label>To:</label>
                            <input type="date"></input>
                        </div>

                        <div className='p-2 g-1 border shadow-sm p-3 mb-5 bg-body rounded'>
                        <ol>
                            {this.state.shipResponse.map((res)=>(
                                <li key={this.state.shipResponse.indexOf(res)} >{res.toString()}</li>    
                            ))
                            }
                            </ol>
                        </div>     

{/* 
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
 */}   

               </div>     
               
            </div>
        </div>
        )
    }
}

export default GeneralView;