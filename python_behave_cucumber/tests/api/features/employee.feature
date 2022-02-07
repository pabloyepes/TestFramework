@create_team
Feature: Employee

  Background:
    Given The "admin" user is logged in

  @deleted_user
  Scenario: Check basic employee flow
    Then All the employees should be properly listed
    When The employees with the following data are created
      | employee_name    | employee_salary | employee_age | profile_image |
      | First Test User  | 1234            | 33           |               |
      | Second Test User | 9999            | 99           | no image      |
    Then The created employees are validated
    And The employee with id "30" is deleted



  Scenario Outline: Check the creation of multiple employees with an outline
    When The employees with the following data are created
      | employee_name | employee_salary | employee_age | profile_image |
      | <name>        | <salary>        | <age>        | <image>       |
    Then The created employees are validated

    Examples:
      | name                | salary | age | image     |
      | Outline 1 Test User | 8000   | 21  | image.png |
      | Outline 2 Test      | 10000  | 30  |           |
      | Outline 3 User      | 50000  | 50  |           |