import React from 'react';
import Department from './Department'


const DepartmentList = ({deptos, onSelectedDepartment}) => {

    const handleDepartmentClick = depto =>{
        console.log("handleDepartmentClick");
        onSelectedDepartment(depto);
    };

    const strToComponent = deptos => {
        return deptos.map( depto => 
            (
                <Department 
                    key={depto.department_id} 
                    depto={depto.name}
                    onDepartmentClick={()=>handleDepartmentClick(depto)}>
                </Department>));
    };
    return (
        <div className="container-fluid list-group-item">
            <h4>Departments</h4>
            {
                strToComponent(deptos)
            }
        </div>
    );
};

export default DepartmentList;