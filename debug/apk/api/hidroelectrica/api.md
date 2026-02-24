# API Endpoint Documentation

Documentarea endpoint-urilor identificate în aplicație.  
Clasificarea este făcută pe baza comportamentului observabil al endpoint-ului (read-only vs side-effect), pe baza naming-ului și a tiparului de apel.

---

### 🟢 Read-Only Endpoints

Aceste endpoint-uri doar returnează date și nu produc modificări de stare.

---

### Billing

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `API/Billing/GetActualBill` | - | `java.lang.String r1 = URL` |
| `API/Billing/GetBillHistory1` | `GET_BILL_SUMMARY` | `q5.a.f(dVar, URL, tag, hashMap, ...)` |
| `API/Billing/GetSchedulePayment` | `GET_SCHEDULED_PAYMENT_LIST` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `API/Billing/GetAvgBill` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Billing/GetMyBudgetBill` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Billing/GetPaymentLocation` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Billing/GetBillPayMode` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Billing/GetBankRouting` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Billing/GetAccountRecurringPayment` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/Billing/GetBill` | `GET_CURRENT_BILL` | `q5.a.f(this, URL, tag, hashMap, ...)` |
| `Service/Billing/GetBillingHistoryList` | `GET_BILL_HISTORY` | `q5.a.f(dVar, URL, tag, hashMap, ...)` |
| `Service/Billing/GetBillPDF` | `GET_CURRENT_BILL_PDF` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `Service/Billing/GetUnpaidInvoiceDetailList` | `GET_UNPAID_INVOICES_LIST` | `q5.a.f(this, URL, tag, hashMap, ...)` |
| `API/Prepaid/GetPrePaidBillData` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Prepaid/GetPaymentDetailsForAccountNumber` | - | `q5.a.f(..., URL, ..., ...)` |
| `PaymentAdapter/api/v1/Payment/GetPaymentDetails` | - | `q5.a.f(..., URL, ..., ...)` |
| `PaymentAdapter/api/v1/Payment/ConvenienceFee` | - | `q5.a.f(..., URL, ..., ...)` |

---

### Account

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `API/Account/GetMyAccountProfile` | `LOAD_CUSTOMER_INFO_TAG` | `q5.a.f(e7, URL, tag, hashMap, ...)` |
| `API/Account/GetMyAccountSetting` | `GET_ACCOUNT_SETTING_INFO` | `q5.a.f(e7, URL, tag, hashMap, ...)` |
| `API/Account/GetUserRole` | `USER_ROLE` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `API/Account/GetPersonalInfo` | `TAG_PERSONAL_INFO` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `API/Account/GetEBilling` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Account/GetDirectDebit` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Account/GetInviteUserData` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Account/GetInviteUserAccountNumber` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Account/LoadState` | - | `q5.a.f(..., URL, ..., ...)` |

---

### Usage & Metering

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `Service/Usage/GetMultiMeter` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/Usage/GetUsageGeneration` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Usage/GetUsageGenerationNew` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Usage/GetCurrentRate` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/IndexHistory/GetMeterCounterSeries` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/IndexHistory/GetMeterReadHistory` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/SelfMeterReading/GetPods` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/SelfMeterReading/GetWindowDates` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/SelfMeterReading/GetMeterValue` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/SelfMeterReading/GetPreviousMeterRead` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/Billing/GetHasNonAMIMeter` | - | `q5.a.f(..., URL, ..., ...)` |

---

### Smart Home

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `API/SmartHome/GetSmartDevices` | `GET_DEVICES` | `q5.a.f(e7, URL, tag, new HashMap(), ...)` |
| `API/SmartHome/GetThermostatURL` | `GET_THERMOSTAT_URL` | `q5.a.f(e7, URL, tag, new HashMap(), ...)` |
| `API/SmartHome/CheckUserThermostatInDb` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/HoneyWell/GetTokenNet` | `GET_HONEYWELL_TOKEN_NET` | `q5.a.f(e7, URL, tag, hashMap, ...)` |
| `API/HoneyWell/GetAllLocations` | `GET_ALL_LOCATION_HONEYWELL` | `q5.a.f(e10, URL, tag, hashMap2, ...)` |
| `API/HoneyWell/GetHoneyWellRefreshToken` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/HoneyWell/GetExistingToken` | - | `q5.a.f(..., URL, ..., ...)` |

---

### Notifications

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `NotificationAPI/Notification/GetInboxMessages` | - | `java.lang.String r5 = URL` |
| `NotificationAPI/Notification/GetMessageBody` | `GET_NOTIFICATIONS_DETAIL` | `q5.a.f(d9, URL, tag, hashMap, ...)` |
| `NotificationAPI/Notification/GetNotificationCount` | `GET_MAIL_COUNT_TAG` | `q5.a.f(c11, URL, tag, hashMap, ...)` |
| `JWTAPI/api/NotificationPreference/GetPreference` | - | `q5.a.f(..., URL, ..., ...)` |

---

### Configuration / Dynamic / Static

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `API/Configuration/GetMultilingual` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Common/GetAllLanguage` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Common/GetValidateAttachment` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Dynamic/SearchZipCodes` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Dynamic/SearchCityOrStates` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Dynamic/GetControlDetailsByTemplate` | - | `q5.a.f(..., URL, ..., ...)` |


---

### 🔴 Write / Side-Effect Endpoints

Aceste endpoint-uri modifică date sau inițiază procese server-side.

---

### Account Management

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `API/Account/SetMyAccountProfile` | `SET_PHONE_EMAIL_TAG` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `API/Account/DeletePersonalData` | `TAG_FORGET_ME` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `API/Account/SetDefaultAccount` | `UPDATE_USER_PROFILE_TAG` | `q5.a.f(e7, URL, tag, hashMap, ...)` |
| `API/Account/SetBillDelivery` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Account/SaveContactAddress` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/Account/UpdatePrimaryEmail` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/Account/DeleteAccount` | `DELETE_ACCOUNT_INFO_TAG` | `q5.a.f(e7, URL, tag, hashMap, ...)` |
| `Service/Account/AddUserAccount` | - | `q5.a.f(..., URL, ..., ...)` |

---

### Payments

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `API/Billing/SetPaymentInfo` | `PRE_LOGIN_PAYMENTS` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `API/Billing/UpdatePaymentInfo` | `UPDATE_DEFAULT_CARD_TAG` | `q5.a.f(e7, URL, tag, hashMap, ...)` |
| `API/Billing/CancelSchedulePayment` | `CANCEL_SCHEDULED_PAYMENT` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `API/Billing/SetAccountRecurringPayment` | - | `q5.a.f(..., URL, ..., ...)` |
| `PaymentAdapter/api/v1/Payment/GooglePayWalletPayment` | `PAY_WITH_GOOGLE_PAY` | `q5.a.f(cVar, URL, tag, hashMap, ...)` |
| `PaymentAdapter/api/v1/Payment/WalletPayment` | `THREE_DS_AUTHORISATION_PAYMENT` | `q5.a.f(cVar2, URL, tag, hashMap, ...)` |

---

### Service Requests

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `API/Service/SubmitServiceRequest` | `SUBMIT_SERVICE_REQUEST` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `API/ContactUs/SetConnectMeRequest` | `SUBMIT_CONNECT_ME_REQUEST` | `q5.a.f(c10, URL, tag, hashMap, ...)` |
| `Service/SelfMeterReading/SubmitSelfMeterRead` | `SUBMIT_SELF_METER_READ` | `q5.a.f(m3, URL, tag, hashMap, ...)` |
| `Service/Registration/SetCustomerRegistration` | - | `q5.a.f(..., URL, ..., ...)` |
| `Service/Registration/ValidateSinglePageRegistration` | - | `q5.a.f(..., URL, ..., ...)` |

---

### 🟡 Authentication / Token / Sensitive

Aceste endpoint-uri sunt sensibile, dar nu reprezintă business write logic.

| URL | Tag Asociat | Apel Tipic |
|------|-------------|------------|
| `API/RequestIdAuthentication/CreateOTP` | `CreateOTP` | `q5.a.f(d9, URL, tag, hashMap, ...)` |
| `API/RequestIdAuthentication/VerifyOTP` | - | `java.lang.String r7 = URL` |
| `API/TwoFactorAuthentication/VerifyUserTwoFactorAuthenticationTokenAsync` | - | `java.lang.String r11 = URL` |
| `API/UserLogin/ValidateUserLogin` | - | `java.lang.String r9 = URL` |
| `API/UserLogin/Logout` | - | `q5.a.f(..., URL, ..., ...)` |
| `API/UserLogin/ChangeUsersPassword` | - | `q5.a.f(..., URL, ..., ...)` |

---

### Observații Tehnice

- Majoritatea apelurilor folosesc wrapper-ul `q5.a.f(...)`
- Există inconsecvență semantică între `Service/` și `API/`
- Existența endpoint-urilor `GetSet*` (ex: `GetSetFeature`, `GetSetHighUsageAlert`) indică design REST slab
- Lipsa separării clare GET vs POST la nivel semantic poate genera risc de abuz sau configurare greșită la nivel de gateway
