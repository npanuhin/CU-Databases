<h1 align="center">HW5</h1>


<div align="center">

| **ID** | **Cust_name** | **Phone** | **Prod_ID** | **P_name** | **Cat**     | **Date**   | **Qty** | **PricePerUnit** | **TotalPrice** |
|--------|---------------|-----------|-------------|------------|-------------|------------|---------|------------------|----------------|
| 1      | John Doe      | 12345678  | P101        | Laptop     | Electronics | 2024-03-01 | 1       | 1000             | 1000           |
| 2      | Jane Smith    | 98765432  | P102        | Phone      | Electronics | 2024-03-02 | 2       | 500              | 1000           |
| 3      | John Doe      | 12345678  | P103        | Tablet     | Electronics | 2024-03-05 | 1       | 300              | 300            |
| 4      | Jane Smith    | 98765432  | P101        | Laptop     | Electronics | 2024-03-06 | 1       | 1000             | 1000           |
| 5      | Mark Lee      | 55577799  | P104        | Speaker    | Accessories | 2024-03-07 | 3       | 50               | 150            |
| 6      | Emily Clark   | 22233344  | P102        | Phone      | Electronics | 2024-03-08 | 1       | 500              | 500            |
| 7      | Alex Brown    | 66699988  | P105        | Monitor    | Electronics | 2024-03-09 | 2       | 200              | 400            |
| 8      | Mark Lee      | 55577799  | P106        | Phone      | Accessories | 2024-03-10 | 1       | 80               | 80             |
| 9      | Emily Clark   | 22233344  | P101        | Laptop     | Electronics | 2024-03-11 | 1       | 1000             | 1000           |
| 10     | John Doe      | 12345678  | P104        | Speaker    | Accessories | 2024-03-12 | 2       | 50               | 100            |

</div>

## 1NF

`1NF` Rules:
- ✔️ Each table cell should contain a single value — True for all cells
- ✔️ Each record needs to be unique — True for all records

`1NF`: **No Changes Required**

## 2NF

`2NF` Rules:
- ✔️ The tables are in 1NF — True, due to the previous step
- ✔️ There is no partial dependencies — `ID` is the primary key, and all other columns are fully dependent on it

`2NF`: **No Changes Required**

## 3NF

`3NF` Rules:
- ✔️ The tables are in 2NF — True, due to the previous step
- ❌ There is no transitive dependencies:
	- `Phone` should be dependent on `Cust_name`
	- `P_name`, `Cat` and `PricePerUnit` should be dependent on `Prod_ID`
	- (?) `TotalPrice` should be dependent solely on the order (`Qty` and the product)


`3NF`:

<table width="100%">
<tr width="100%">
<td width="100%">

<div align="center">

**Table `Orders`**

| **Order_ID** | **Cust_ID** | **Prod_ID** | **Date**     | **Qty** | **TotalPrice** |
|--------------|-------------|-------------|--------------|---------|----------------|
| 1            | 1           | P101        | 2024-03-01   | 1       | 1000           |
| 2            | 2           | P102        | 2024-03-02   | 2       | 1000           |
| 3            | 1           | P103        | 2024-03-05   | 1       | 300            |
| 4            | 2           | P101        | 2024-03-06   | 1       | 1000           |
| 5            | 3           | P104        | 2024-03-07   | 3       | 150            |
| 6            | 4           | P102        | 2024-03-08   | 1       | 500            |
| 7            | 5           | P105        | 2024-03-09   | 2       | 400            |
| 8            | 3           | P106        | 2024-03-10   | 1       | 80             |
| 9            | 4           | P101        | 2024-03-11   | 1       | 1000           |
| 10           | 1           | P104        | 2024-03-12   | 2       | 100            |

</div>

</td>
<td width="100%">

<div align="center">

**Table `Customers`**

| **Cust_ID** | **Cust_name** | **Phone** |
|-------------|---------------|-----------|
| 1           | John Doe      | 12345678  |
| 2           | Jane Smith    | 98765432  |
| 3           | Mark Lee      | 55577799  |
| 4           | Emily Clark   | 22233344  |
| 5           | Alex Brown    | 66699988  |

</div>

</td>
</tr>
<tr>
<td>

<div align="center">

**Table `Products`**

| **Prod_ID** | **P_name** | **Cat_ID** | **PricePerUnit** |
|-------------|------------|------------|------------------|
| P101        | Laptop     | 1		    | 1000             |
| P102        | Phone      | 1		    | 500              |
| P103        | Tablet     | 1		    | 300              |
| P104        | Speaker    | 2		    | 50               |
| P105        | Monitor    | 1		    | 200              |
| P106        | Phone      | 2		    | 80               |

</div>

</td>
<td>

<div align="center">

**Table `Categories`**

| **Cat_ID**  | **Cat**     |
|-------------|-------------|
| 1           | Electronics |
| 2           | Accessories |

</div>

</td>
</tr>
</table>
