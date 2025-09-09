package com.example.jdbc_demo.service;

import com.example.jdbc_demo.entity.Employee;
import com.example.jdbc_demo.repository.DepartmentRepository;
import com.example.jdbc_demo.repository.EmployeeRepository;
import com.example.jdbc_demo.util.JsonFileUtil;
import com.example.jdbc_demo.util.SqlFileUtil;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.*;

@Service
public class QueryService {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private JsonFileUtil jsonFileUtil;

    @Autowired
    private EmployeeRepository employeeRepository;

    @Autowired
    private DepartmentRepository departmentRepository;

    // Fetch all employees
    public List<Map<String, Object>> getAllEmployees() {
        String sql = "SELECT * FROM employees";
        return jdbcTemplate.queryForList(sql);
    }

    // Fetch all dependents
    public List<Map<String, Object>> getAllDependents() {
        String sql = "SELECT * FROM dependents";
        return jdbcTemplate.queryForList(sql);
    }

    // Fetch employees with department and project details
    public List<Map<String, Object>> getEmployeeDetails() {
        String sql = "SELECT e.id, e.name, e.gender, e.address, e.dob, e.doj, e.designation, " +
                "d.name AS department_name, d.location AS department_location, " +
                "p.name AS project_name, p.location AS project_location " +
                "FROM employees e " +
                "LEFT JOIN departments d ON e.department_id = d.id " +
                "LEFT JOIN projects p ON e.project_id = p.id";
        return jdbcTemplate.queryForList(sql);
    }

    // Fetch dependents of a given employee
    public List<Map<String, Object>> getDependentsByEmployeeId(Integer employeeId) {
        String sql = "SELECT dep.id, dep.name, dep.gender, dep.location, dep.relationship " +
                "FROM dependents dep " +
                "WHERE dep.employee_id = ?";
        return jdbcTemplate.queryForList(sql, employeeId);
    }

    public List<Map<String, Object>> runQueryFromFile(String sqlFile) throws Exception {
        String sql = SqlFileUtil.readSqlFile(sqlFile + ".sql");
        return jdbcTemplate.queryForList(sql);
    }

    public List<JsonNode> runQueryWithTemplate(String sqlFileName, String jsonFileName) throws IOException {
        // Read SQL
        String sqlQuery = SqlFileUtil.readSqlFile(sqlFileName + ".sql");

        // Run SQL
        List<Map<String, Object>> rows = jdbcTemplate.queryForList(sqlQuery);

        // Read JSON template
        String jsonTemplate = jsonFileUtil.readJsonFile(jsonFileName + ".json");
        JsonNode templateNode = objectMapper.readTree(jsonTemplate);

        List<JsonNode> result = new ArrayList<>();

        for (Map<String, Object> row : rows) {
            // Deep copy template
            ObjectNode rowNode = objectMapper.createObjectNode();
            fillTemplate(rowNode, templateNode, row);
            result.add(rowNode);
        }

        return result;
    }

    private void fillTemplate(ObjectNode target, JsonNode template, Map<String, Object> row) {
        template.fields().forEachRemaining(entry -> {
            String key = entry.getKey();
            JsonNode value = entry.getValue();

            if (value.isObject()) {
                // Nested object → recurse
                ObjectNode nestedNode = objectMapper.createObjectNode();
                fillTemplate(nestedNode, value, row);
                target.set(key, nestedNode);
            } else {
                // Leaf node → replace with DB value
                String columnName = value.asText();
                Object columnValue = row.get(columnName);
                if (columnValue != null) {
                    target.put(key, columnValue.toString());
                } else {
                    target.putNull(key);
                }
            }
        });
    }
}
