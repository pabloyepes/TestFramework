Feature: Search

  @smoke
  Scenario: Search for a product and add it to the cart
    When The product "car" is searched
    Then All the results should match with my search
    And The result "Car RTR" is opened
    Then The product image should load
    When The product "laptop" is searched
    And The result in the position "3" is opened
    Then The product image should load
    When The product "bed" is searched
    And A random result is opened
    Then The product image should load