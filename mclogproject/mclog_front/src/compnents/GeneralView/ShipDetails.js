import React from 'react'
import { ReactDOM } from 'react'
import './ShipDetails.css'
import 'axios'
import axios from 'axios'

function GetShipByImo(props){
        // GET request - ship by imo 
        // Return data
        axios.get('http://127.0.0.1:8000/search')
        .then((response)=>{
            console.log(response);
        })

}

class GeneralView extends React.Component{
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
                                <option>From db</option>
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
                        <select name='Scenario'>
                            <option>From db</option>
                        </select>
                        </div>

                    </div>                    
                </div>
                <div className="row align-items-end">
                    <div className="col">
                        <p>
                            Placeholder for the chart
                        </p>
                        <div>
                            <GetShipByImo/>
                        </div>
                     </div>
                </div>
            </div>

            
        )
    }
}

export default GeneralView;