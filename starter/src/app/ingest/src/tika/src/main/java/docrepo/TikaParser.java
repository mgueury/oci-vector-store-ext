package docrepo;

import com.oracle.bmc.Region;
import com.oracle.bmc.auth.AuthenticationDetailsProvider;
import com.oracle.bmc.auth.InstancePrincipalsAuthenticationDetailsProvider;
import com.oracle.bmc.objectstorage.requests.GetObjectRequest;
import com.oracle.bmc.objectstorage.requests.PutObjectRequest;
import com.oracle.bmc.objectstorage.responses.GetObjectResponse;
import com.oracle.bmc.objectstorage.responses.PutObjectResponse;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Future;

import com.oracle.bmc.responses.AsyncHandler;
import com.oracle.bmc.objectstorage.ObjectStorageAsyncClient;

import com.oracle.bmc.streaming.StreamClient;
import com.oracle.bmc.streaming.model.PutMessagesDetails;
import com.oracle.bmc.streaming.model.PutMessagesDetailsEntry;
import com.oracle.bmc.streaming.model.PutMessagesResultEntry;
import com.oracle.bmc.streaming.model.Stream;
import com.oracle.bmc.streaming.StreamAdminClient;

import com.oracle.bmc.streaming.requests.GetStreamRequest;
import com.oracle.bmc.streaming.requests.ListStreamsRequest;
import com.oracle.bmc.streaming.requests.PutMessagesRequest;
import com.oracle.bmc.streaming.responses.GetStreamResponse;
import com.oracle.bmc.streaming.responses.ListStreamsResponse;
import com.oracle.bmc.streaming.responses.PutMessagesResponse;
import com.oracle.bmc.util.internal.StringUtils;
import com.oracle.bmc.objectstorage.ObjectStorage;
import com.oracle.bmc.objectstorage.ObjectStorageClient;
import org.apache.tika.Tika;
import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.xml.sax.SAXException;

import javax.json.*;
import java.util.ArrayList;
import java.util.List;
import java.nio.charset.StandardCharsets;

import org.apache.http.conn.ssl.*;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.*;

import static java.nio.charset.StandardCharsets.UTF_8;

import javax.net.ssl.*;
import java.io.*;
import java.net.URL;
import java.security.*;
import java.security.cert.*;

public class TikaParser {
    private ObjectStorage objectStorageClient;
    private InstancePrincipalsAuthenticationDetailsProvider provider;

    public TikaParser() {
        initOciClients();
    }

    private void initOciClients() {
        System.err.println("Inside initOciClients");
        try {
            provider = InstancePrincipalsAuthenticationDetailsProvider.builder().build();
            System.err.println("InstancePrincipalsAuthenticationDetailsProvider setup");
            objectStorageClient = ObjectStorageClient.builder().build(provider);
            // objectStorageClient.setRegion(Region.EU_FRANKFURT_1);
            System.err.println("ObjectStorage client setup");

        } catch (Exception ex) {
            System.err.println("Exception " + ex.getMessage());
            ex.printStackTrace();
            throw new RuntimeException("failed to init oci clients", ex);
        }
    }

    public GetObjectResponse readObject(String namespace, String bucketname, String filename) {
        try {
            GetObjectRequest getObjectRequest = GetObjectRequest.builder()
                    .namespaceName(namespace)
                    .bucketName(bucketname)
                    .objectName(filename)
                    .build();
            GetObjectResponse getObjectResponse = objectStorageClient.getObject(getObjectRequest);
            return getObjectResponse;
        } catch (Exception e) {
            throw new RuntimeException("Could not read from os!" + e.getMessage());
        }
    }

    public JsonObject parseObject(GetObjectResponse objectResponse)
            throws IOException, TikaException, SAXException {
        // Create a Tika instance with the default configuration
        Tika tika = new Tika();
        Metadata metadata = new Metadata();
        Reader reader = tika.parse(objectResponse.getInputStream(), metadata);
        objectResponse.getInputStream().close();
        JsonObjectBuilder jsonObjectBuilder = Json.createObjectBuilder();
        // getting metadata of the document
        String[] metadataNames = metadata.names();
        for (String name : metadataNames) {
            jsonObjectBuilder.add(name, metadata.get(name));
        }
        // getting the content of the document
        BufferedReader bufferedReader = new BufferedReader(reader);
        StringBuilder stringBuilder = new StringBuilder();
        String line;
        while ((line = bufferedReader.readLine()) != null) {
            stringBuilder.append(line);
        }
        String content = stringBuilder.toString();
        bufferedReader.close();
        jsonObjectBuilder.add("content", content);
        JsonObject jsonObject = jsonObjectBuilder.build();

        return jsonObject;
    }

    public static void main(String[] args) {
        if (args.length<3 ) {
            System.err.println( "Missing arguments: namespace, bucketName, resourceName" );
            return;
        }
        String namespace = args[0];
        String bucketName = args[1];
        String resourceName = args[2];
        System.err.println("resourceName=" + resourceName);
        try {
            TikaParser parser = new TikaParser();
            GetObjectResponse getObjectResponse = parser.readObject(namespace, bucketName, resourceName);
            JsonObject jsondoc = parser.parseObject(getObjectResponse);
            System.out.println( jsondoc.toString() ); // "ok";
        } catch (Exception ex) {
            System.err.println("Exception " + ex.getMessage());
            ex.printStackTrace();
            System.err.println( "Exception in TikaObjectStorage: " + ex.getMessage() );
            return;
        }
    }
}
