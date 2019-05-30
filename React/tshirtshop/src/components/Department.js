import React from 'react';


const Department = (props) => {
    const {depto} = props;
    const {onDepartmentClick} = props;
    return (
    <div className="locationCont" onClick={onDepartmentClick}>
        <button className="bttn list-group-bttn">{depto}</button>
    </div>
    )
};

export default Department;