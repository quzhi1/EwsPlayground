package main

import (
	"bytes"
	"context"
	"encoding/base64"
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/rs/zerolog/log"
)

const (
	hostname = "https://ex.mail.ovh.ca"
	port     = 443
)

var (
	username = os.Getenv("EWS_OVH_USERNAME")
	password = os.Getenv("EWS_OVH_PASSWORD")
)

func main() {
	ctx := log.Logger.With().Logger().WithContext(context.Background())
	// Encode the credentials for basic authentication
	auth := base64.StdEncoding.EncodeToString([]byte(username + ":" + password))

	// SOAP request body
	soapBody := `<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
<soap:Body>
<GetFolder xmlns="http://schemas.microsoft.com/exchange/services/2006/messages"
		   xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types">
  <FolderShape>
	<t:BaseShape>Default</t:BaseShape>
  </FolderShape>
  <FolderIds>
	<t:DistinguishedFolderId Id="inbox"/>
  </FolderIds>
</GetFolder>
</soap:Body>
</soap:Envelope>`
	ewsUrl := ensureHttpScheme(hostname) + ":" + strconv.Itoa(port) + "/EWS/Exchange.asmx"
	// Create a new HTTP request
	req, err := http.NewRequest("POST", ewsUrl, bytes.NewBuffer([]byte(soapBody)))
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msgf("Login: Failed connecting to EWS server '%s'", ewsUrl)
		panic("Failed connecting to EWS server")
	}

	// Set the necessary request headers
	req.Header.Add("Content-Type", "text/xml; charset=utf-8")
	req.Header.Add("Authorization", "Basic "+auth)
	req.Header.Add("SOAPAction", "http://schemas.microsoft.com/exchange/services/2006/messages/GetFolder")

	// Initialize HTTP client and send the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msgf("Login: Error sending request: %s", err)
		panic(err)
	}
	defer resp.Body.Close()

	// Read and print the response
	_, err = io.ReadAll(resp.Body)
	if err != nil {
		log.Ctx(ctx).Error().Err(err).Msgf("Login: Error reading response body: %s", err)
		panic(err)
	}

	if resp.StatusCode != http.StatusOK {
		switch resp.StatusCode {
		case http.StatusUnauthorized:
			log.Ctx(ctx).Error().Msgf("Login: Failed validating credentials on EWS server")
			panic("Failed validating credentials on EWS server")
		default:
			log.Ctx(ctx).Error().Msgf("Login: Failed connecting to EWS server. Server returned status code %d", resp.StatusCode)
			panic(fmt.Sprintf("Failed connecting to EWS server. Server returned status code %d", resp.StatusCode))
		}
	}
}

// ensureHttpScheme Ensure the URL has a scheme (http:// or https://)
func ensureHttpScheme(url string) string {
	if !strings.HasPrefix(url, "http://") && !strings.HasPrefix(url, "https://") {
		// Default to https if no scheme is specified
		url = "https://" + url
	}
	return url
}
