import React from 'react'
import { ReactDOM } from 'react'
import './ShipDetails.css'


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
                            <select name='IMO'>
                                <option>From db</option>
                            </select>
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
                     </div>
                </div>
            </div>

            
        )
    }
}

export default GeneralView;