<h1 align="center">HW3 (Stratascratch)</h1>


## 1. [Share of Active Users](https://platform.stratascratch.com/coding/2005-share-of-active-users):

<details>
<summary>Screenshot</summary>
<img align="center" width="100%" src="Screenshot Task 1.png">
</details>


```sql
SELECT
    100.0 * (
        SELECT count(1)
        FROM fb_active_users
        WHERE country = 'USA' AND status = 'open'
    ) / count(*)
FROM fb_active_users
```

## 2. [Unique Users Per Client Per Month](https://platform.stratascratch.com/coding/2024-unique-users-per-client-per-month):

<details>
<summary>Screenshot</summary>
<img align="center" width="100%" src="Screenshot Task 2.png">
</details>

```sql
SELECT
    client_id,
    EXTRACT(MONTH FROM time_id) AS month,
    COUNT(DISTINCT user_id) AS users_num
FROM fact_events
GROUP BY client_id, month
ORDER BY client_id, month;
```

## 3. [Number of Shipments Per Month](https://platform.stratascratch.com/coding/2056-number-of-shipments-per-month):

<details>
<summary>Screenshot</summary>
<img align="center" width="100%" src="Screenshot Task 3.png">
</details>

```sql
SELECT
    to_char(shipment_date, 'YYYY-MM') AS year_month,
    count(distinct (shipment_id, sub_id))
FROM amazon_shipment
GROUP BY 1
```

## 4. [Premium Accounts](https://platform.stratascratch.com/coding/2097-premium-acounts):

<details>
<summary>Screenshot</summary>
<img align="center" width="100%" src="Screenshot Task 4.png">
</details>

```sql
WITH paying_accounts AS (
    SELECT entry_date, account_id
    FROM premium_accounts_by_day
    WHERE final_price > 0
)
SELECT
    p.entry_date,
    COUNT(DISTINCT p.account_id) AS premium_paid_accounts,
    COUNT(DISTINCT p7.account_id) AS premium_paid_accounts_after_7d
FROM paying_accounts p
LEFT JOIN paying_accounts p7
    ON p.account_id = p7.account_id
    AND p7.entry_date = p.entry_date + INTERVAL '7 days'
GROUP BY p.entry_date
ORDER BY p.entry_date
LIMIT 7;
```

## 5. [Flags per Video](https://platform.stratascratch.com/coding/2102-flags-per-video):

<details>
<summary>Screenshot</summary>
<img align="center" width="100%" src="Screenshot Task 5.png">
</details>

```sql
SELECT
    video_id,
    COUNT(DISTINCT CONCAT(COALESCE(user_firstname, ''), COALESCE(user_lastname, ''))) AS num_unique_users
FROM user_flags
WHERE flag_id IS NOT NULL
GROUP BY video_id;
```
