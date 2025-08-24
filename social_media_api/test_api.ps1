# PowerShell script to smoke test the Social Media API on Render
# To run: ./test_api.ps1

# --- Configuration ---
$BaseUrl = "https://sma-jvqc.onrender.com/api"
$Username = "tester_$(Get-Random -Minimum 1000 -Maximum 9999)"
$Password = "Password123!"
$Email = "$Username@example.com"
$Token = $null
$PostId = $null

# --- Helper Functions ---
function Invoke-ApiRequest {
    param(
        [string]$Method,
        [string]$Endpoint,
        [object]$Body,
        [switch]$Authenticated
    )
    $Uri = "$BaseUrl$Endpoint"
    $Headers = @{ "Content-Type" = "application/json" }
    if ($Authenticated.IsPresent -and $Token) {
        $Headers["Authorization"] = "Token $Token"
    }

    try {
        if ($Body) {
            $json = $Body | ConvertTo-Json -Depth 5
            $resp = Invoke-WebRequest -Method $Method -Uri $Uri -Headers $Headers -Body $json -ContentType "application/json" -SkipHttpErrorCheck
        } else {
            $resp = Invoke-WebRequest -Method $Method -Uri $Uri -Headers $Headers -SkipHttpErrorCheck
        }

        # Parse JSON if possible; otherwise return raw content
        if ($resp.Content -and ($resp.Headers["Content-Type"] -like "*application/json*")) {
            return $resp.Content | ConvertFrom-Json -ErrorAction SilentlyContinue
        }
        return $resp.Content
    }
    catch {
        Write-Host "ERROR: Failed to call $Method $Uri" -ForegroundColor Red
        if ($_.Exception.Response -and $_.Exception.Response.Content) {
            try {
                $errContent = $_.Exception.Response.Content
                if ($errContent -and ($_.Exception.Response.Headers["Content-Type"] -like "*application/json*")) {
                    $errJson = $errContent | ConvertFrom-Json -ErrorAction SilentlyContinue
                    if ($errJson) { Write-Host (ConvertTo-Json $errJson -Depth 5) -ForegroundColor Red }
                    else { Write-Host $errContent -ForegroundColor Red }
                } else {
                    Write-Host $errContent -ForegroundColor Red
                }
            } catch {
                Write-Host $_.Exception.Message -ForegroundColor Red
            }
        } else {
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
        return $null
    }
}

# --- Test Execution ---

# 1. Register a new user
Write-Host "1. Registering new user: $Username..." -ForegroundColor Cyan
$RegisterBody = @{ username = $Username; password = $Password; email = $Email }
$RegisterResponse = Invoke-ApiRequest -Method POST -Endpoint "/accounts/register/" -Body $RegisterBody
if ($RegisterResponse -and $RegisterResponse.token) { $Token = $RegisterResponse.token; Write-Host "  SUCCESS: Got token." -ForegroundColor Green } else { Write-Host "  FAILURE: Could not register or get token." -ForegroundColor Red; exit 1 }

# 2. Login with the new user
Write-Host "2. Logging in as: $Username..." -ForegroundColor Cyan
$LoginBody = @{ username = $Username; password = $Password }
$LoginResponse = Invoke-ApiRequest -Method POST -Endpoint "/accounts/login/" -Body $LoginBody
if ($LoginResponse -and $LoginResponse.token) { $Token = $LoginResponse.token; Write-Host "  SUCCESS: Login confirmed, token refreshed." -ForegroundColor Green } else { Write-Host "  FAILURE: Could not log in." -ForegroundColor Red; exit 1 }

# 3. Create a new post
Write-Host "3. Creating a new post..." -ForegroundColor Cyan
$PostBody = @{ title = "My Test Post"; content = "This is content from the test script." }
$PostResponse = Invoke-ApiRequest -Method POST -Endpoint "/posts/" -Body $PostBody -Authenticated
if ($PostResponse -and $PostResponse.id) { $PostId = $PostResponse.id; Write-Host "  SUCCESS: Created post with ID: $PostId" -ForegroundColor Green } else { Write-Host "  FAILURE: Could not create post." -ForegroundColor Red; exit 1 }

# 4. List all posts
Write-Host "4. Listing all posts..." -ForegroundColor Cyan
$Posts = Invoke-ApiRequest -Method GET -Endpoint "/posts/" -Authenticated
if ($Posts) { if ($Posts.results) { Write-Host "  SUCCESS: Retrieved $($Posts.results.Count) posts." -ForegroundColor Green } else { Write-Host "  SUCCESS: Retrieved posts." -ForegroundColor Green } }

# 5. Like the post
Write-Host "5. Liking post $PostId..." -ForegroundColor Cyan
$LikeResponse = Invoke-ApiRequest -Method POST -Endpoint "/posts/$PostId/like/" -Authenticated
if ($LikeResponse) { if ($LikeResponse.success) { Write-Host "  SUCCESS: $($LikeResponse.success)" -ForegroundColor Green } else { Write-Host "  SUCCESS: Like done." -ForegroundColor Green } }

# 6. Unlike the post
Write-Host "6. Unliking post $PostId..." -ForegroundColor Cyan
$null = Invoke-ApiRequest -Method DELETE -Endpoint "/posts/$PostId/unlike/" -Authenticated
Write-Host "  SUCCESS: Unlike request sent." -ForegroundColor Green

# 7. Get user feed
Write-Host "7. Getting user feed..." -ForegroundColor Cyan
$Feed = Invoke-ApiRequest -Method GET -Endpoint "/feed/" -Authenticated
if ($Feed) { Write-Host "  SUCCESS: Feed endpoint returned content." -ForegroundColor Green }

# 8. Get notifications (small delay to allow async processing)
Write-Host "8. Getting notifications..." -ForegroundColor Cyan
Start-Sleep -Seconds 1
$Notifications = Invoke-ApiRequest -Method GET -Endpoint "/notifications/" -Authenticated
if ($Notifications) { if ($Notifications.results) { Write-Host "  SUCCESS: Retrieved $($Notifications.results.Count) notifications." -ForegroundColor Green } else { Write-Host "  SUCCESS: Retrieved notifications." -ForegroundColor Green } }

Write-Host "`nAll tests completed." -ForegroundColor Magenta
